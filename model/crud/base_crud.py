from decimal import Decimal
from settings.pages.pages import pages
from datetime import datetime
from settings.logger.logger import logger
from sqlalchemy.orm import load_only
from settings.pages.condition import Condition
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy import func, and_, or_, desc, asc, distinct, inspect


class BaseCurd:

    def __init__(self, db, model):
        self.db = db
        self.model = model

    def query_(self, info):
        '''
            in:
                {
                    'curd':{具体搜索的字段} 也可以为False,
                    'all_field': 是否返回所有字段,
                    'reverse': True 输出去除该列表里面的字段 / False 输出只有该列表里面的字段,
                    'query_type': 'and/or',  # 搜索类型
                    'export': [不需要返回的字段/需要返回的字段],
                    'is_first': True/False 单条数据或者多条分页数据,
                    'group_sort': {
                        'group_by': '分组字段',   # 是否分组
                        'sort_by': '排序字段',    # 排序字段
                        'sort_order': '升降序',    # asc:生序/desc:降序
                    },
                    'pagination': {
                            'current':current,  当前第几页
                            'page_size':page_size  每页多少数据
                    }
                }
            out: {'code': '100200', 'msg': '👌', 'data':{'list':[{},{},,,],'pagination':{} } }
        '''
        conditions = []
        if 'start_time' in info and 'end_time' in info:
            start_time = datetime.strftime(info['start_time'], '%Y-%m-%d')
            end_time = datetime.strftime(info['end_time'], '%Y-%m-%d')
            conditions.append(self.model.create_time.between(start_time, end_time))

        curd_dict = info.get('curd')
        if isinstance(curd_dict, dict) and curd_dict:
            for item in info['curd']:
                if isinstance(info['curd'][item], list):
                    conditions.append(getattr(self.model, item).in_(info['curd'][item]))
                else:
                    conditions.append(Condition(self.model).process_condition(item, info['curd'][item]))

        # 构造查询
        if conditions:
            if info.get('query_type') == 'or':
                db_query = self.db.query(self.model).filter(or_(*conditions))
            if info.get('query_type') == 'and':
                db_query = self.db.query(self.model).filter(and_(*conditions))
        else:
            db_query = self.db.query(self.model)

        aggregate_fields = info.get("aggregates")
        aggregate_data = {}

        if aggregate_fields:
            agg_funcs = {
                "sum": func.sum,    # 字段值相加
                "avg": func.avg,    # 平均值
                "max": func.max,    # 最大
                "min": func.min,    # 最小
                "count": func.count     # 数量
            }
            selected_aggregates = []

            for agg_type, fields in aggregate_fields.items():
                if agg_type in agg_funcs:
                    for field in fields:
                        model_field = getattr(self.model, field, None)
                        if model_field is not None:
                            selected_aggregates.append(agg_funcs[agg_type](model_field).label(f"{agg_type}_{field}"))

            if selected_aggregates:
                agg_query = self.db.query(*selected_aggregates)
                if conditions:
                    agg_query = agg_query.filter(and_(*conditions))
                try:
                    result = agg_query.first()
                    if result:
                        aggregate_data = dict(result._mapping)
                except Exception as e:
                    logger.warning(f"聚合字段查询失败: {e}")

        if info['group_sort']:
            # 添加分组
            if 'group_by' in info['group_sort']:
                group_field = getattr(self.model, info['group_sort']['group_by'], None)
                if group_field:
                    db_query = db_query.group_by(group_field)

            # 添加排序
            if 'sort_by' in info['group_sort']:
                sort_field = getattr(self.model, info['group_sort']['sort_by'], None)
                if sort_field:
                    order_direction = desc if info['group_sort'].get('sort_order', 'asc') == 'desc' else asc
                    db_query = db_query.order_by(order_direction(sort_field))

        # 所有的字段
        base_export = self.model.__table__.columns.keys()
        # 是否返回所有字段
        info['all_field'] = info['all_field'] if 'all_field' in info else True
        # True 输出去除该列表里面的字段 / False 输出只有该列表里面的字段
        info['reverse'] = info['reverse'] if 'reverse' in info else True

        if info['all_field']:
            info['export'] = base_export
        else:
            info['export'] = info['export'] if 'export' in info else base_export

        # 返回单条数据
        if info['is_first']:
            try:
                db_info = db_query.first() if db_query else None
                if db_info:
                    return {'code': 200, 'message': '搜索成功!', 'info': db_info.to_dict(exclude=info['export'], reverse=info['reverse'])}

                if db_info is None:
                    return {'code': 404, 'message': '搜索到数据为空!'}

            except OperationalError as error:
                logger.error(f'搜索出错! 模型: {self.model} 数据: {info} 报错信息: {error}')
                return {'code': 405, 'message': '搜索出错!'}

        # 返回多条数据
        else:
            try:
                # 总数据量
                # 如果包含分组逻辑
                if 'group_by' in info['group_sort'] and getattr(self.model, info['group_sort']['group_by'], None):
                    # 计算分组后的总组数
                    total_query = self.db.query(func.count(distinct(getattr(self.model, info['group_sort']['group_by']))))
                else:
                    # 计算未分组的总数据量 优化 TODO
                    # total_query = self.db.query(func.count(self.model.id))
                    pk_field = inspect(self.model).primary_key[0].name
                    total_query = self.db.query(func.count(getattr(self.model, pk_field)))

                if conditions:
                    total_query = total_query.filter(and_(*conditions))

                query_count = total_query.scalar()

                pagination = pages.iPagination({
                    'current': info['pagination']['current'],
                    'page_size': info['pagination']['page_size'],
                    'total': query_count
                })

                db_info = db_query.offset(info['pagination']['page_size'] * (info['pagination']['current'] - 1)).limit(info['pagination']['page_size']).all()

                if db_info:
                    return {
                        'code': 200,
                        'message': '搜索成功!',
                        'list': [i.to_dict(exclude=info['export'], reverse=info['reverse']) for i in db_info],
                        'pagination': pagination,
                        'aggregates': aggregate_data  # ✅ 加这一行
                    }
                else:
                    return {'code': 404, 'message': '搜索到数据为空!', 'list': [], 'pagination': pagination}

            except Exception as error:
                self.db.rollback()
                logger.error(f'添加数据错误! 模型: {self.model} 数据: {info} 报错信息: {error}')
                return {'code': 404, 'message': '查询出错!', 'info': f'{error}'}

    def create_(self, info):
        try:
            if isinstance(info['curd'], list):
                self.db.bulk_insert_mappings(self.model, info['curd'])
                count = len(info['curd'])

                if info['is_commit']:
                    self.db.commit()
                    self.db.flush()
                return {'code': 200, 'message': '新增成功!', 'info': f'新增了{count}条数据!'}

            if isinstance(info['curd'], dict):
                db_add = self.model()
                for key, value in info['curd'].items():
                    setattr(db_add, key, value)

                self.db.add(db_add)
                if info['is_commit']:
                    self.db.commit()
                    self.db.flush()
                    self.db.refresh(db_add)
                    info = db_add.to_dict()

                return {'code': 200, 'message': '新增成功!', 'info': db_add.to_dict()}

        except IntegrityError as error:
            self.db.rollback()
            logger.error(f'添加数据错误! 模型: {self.model} 数据: {info} 报错信息: {error}')
            print(error)
            return {'code': 400, 'message': '出现重复数据!'}

        except Exception as error:
            self.db.rollback()
            import traceback
            print("完整异常信息：", traceback.format_exc())
            logger.error(f'添加数据错误! 模型: {self.model} 数据: {info} 报错信息: {error}')
            return {'code': 401, 'message': '出现未知错误! 已通知管理员!'}

    def update_(self, info):
        '''
            in：{
                'query:{查询的字段}
                'curd':{里面为要增加或者更新的字段},
                'is_commit':'是否提交'
                }
            out：一个增加或者更新数据后的对象
        '''
        try:
            if isinstance(info['curd'], dict):
                query = self.db.query(self.model)
                for key, value in info['query'].items():
                    query = query.filter(getattr(self.model, key) == value)

                db_obj = query.first()
                if db_obj:

                    for key, value in self.decimal_fields(info['curd']).items():
                        setattr(db_obj, key, value)

                    if info['is_commit']:
                        self.db.commit()
                        self.db.flush()
                        self.db.refresh(db_obj)

                        data_info = db_obj.to_dict()
                        if 'password' in data_info:
                            del data_info['password']

                    return {'code': 200, 'message': '更新成功!'}

                    # return {'code': 400, 'message': '参数不全!'}

                else:
                    return {'code': 404, 'message': '查询参数有错,查询不到数据!'}

            if isinstance(info['curd'], list):
                self.db.bulk_update_mappings(self.model, info['curd'])
                if info['is_commit']:
                    self.db.commit()
                    self.db.flush()
                return {'code': 200, 'message': '更新成功!'}

        except Exception as error:
            if info['is_commit']:
                self.db.rollback()
                logger.info(f'更新数据错误! 模型: {self.model} 数据: {info} 报错信息: {error}')
                return {'code': 400, 'message': '出现错误,请联系管理员!'}
            else:
                self.db.rollback()
                raise  # ✅ 原样抛出，不吃掉

    def remove_(self, info):
        '''
            删除操作
            in: {
                'curd':{}
                'is_commit': '是否提交'
                'is_bulk': '是否批量删除'
                }
            out: 一个删除后的数据对象
        '''
        try:
            query = self.db.query(self.model)
            for key, value in info['curd'].items():
                query_ = query.filter(getattr(self.model, key) == value)

            if info['is_bulk']:
                db_del = query_.all()
            else:
                db_del = query_.first()

            if not db_del:
                return {'code': 404, 'message': '查询不到要删除的数据!'}

            info['is_commit'] = info['is_commit'] if 'is_commit' in info else False
            if info['is_commit']:
                if info['is_bulk']:
                    for obj in db_del:
                        self.db.delete(obj)
                else:
                    self.db.delete(db_del)
                self.db.commit()
                self.db.flush()
            return {'code': 200, 'message': '删除成功!'}

        except Exception as error:
            self.db.rollback()
            logger.info(f'删除数据错误! 模型: {self.model} 数据: {info} 报错信息: {error}')
            return {'code': 400, 'message': '出现错误,请联系管理员!', 'info': str(error)}
