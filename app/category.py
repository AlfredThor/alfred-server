from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from settings.get_db.get_db import get_db
from model.crud.base_crud import BaseCurd
from model.models.model import Category
from model.scheam.category_scheam import Category_scheam
from settings.verify_token.verify_token import get_token_header


class Category_router(APIRouter):
    def __init__(self):
        super().__init__()
        common_dependencies = [Depends(get_token_header)]
        self.add_api_route("/list", self.category_list, methods=["GET"], summary='分类列表', dependencies=common_dependencies)
        self.add_api_route("/add", self.category_add, methods=["POST"], summary='添加分类', dependencies=common_dependencies)
        self.add_api_route("/change/{id}", self.category_change, methods=["PUT"], summary='修改分类', dependencies=common_dependencies)
        self.add_api_route("/delete/{id}", self.category_remove, methods=["DELETE"], summary='删除分类', dependencies=common_dependencies)

    async def category_list(self, type_: int, auth_name: str = None, start_time: str = None, end_time: str = None, sort_by: str = 'create_time',sort_order: str = 'asc',current: int = 1,page_size: int = 20,db: Session = Depends(get_db),):
        # 搜索文章分類
        search_dict = {
            'curd': False,  # 搜索的字段
            'all_field': True,  # 是否返回所有字段
            'reverse': False,  # 是否反转
            'query_type': 'and',  # 搜索类型
            'export': [
                'work_type','serial','user_name','equipment','card_type','card_country','card_code','card_balance',
                'acquisition','rate'],  # 反转的字段
            'group_sort': {
                'group_by': 'id',  # 是否分组
                'sort_by': sort_by,  # 排序字段
                'sort_order': sort_order,  # asc:生序/desc:降序
            },
            'is_first': True if type_ == 0 else False,  # 是否返回一条数据
            'pagination': {'current': current, 'page_size': page_size},  # 分页 current:第几页/page_size:每页多少数据
            'aggregates': {
                'sum': ['card_balance'],
                'avg': ['card_rate', 'rate'],
            }
        }

        curd = {}
        if auth_name:
            curd['auth_name'] = auth_name

        if len(curd) != 0:
            search_dict['curd'] = curd

        if start_time:
            search_dict['start_time'] = start_time

        if end_time:
            search_dict['end_time'] = end_time

        return await BaseCurd(db, Category).query_(search_dict)

    async def category_add(self, item: Category_scheam, db: Session = Depends(get_db)):
        # 添加分类
        return BaseCurd(db, Category).create_({'curd': item.dict(), 'is_commit': True})

    async def category_change(self, id: int, item: Category_scheam, db: Session = Depends(get_db)):
        # 修改分类
        return BaseCurd(db, Category).update_({'query': {'id': id}, 'curd': item.dict(), 'is_commit': True})

    async def category_remove(self, id: int, db: Session = Depends(get_db)):
        # 删除分类
        return BaseCurd(db, Category).update_({'query': {'id': id}, 'curd': {'status':0}, 'is_commit': True})


category_router = Category_router()