from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from model.models.model import Donation
from settings.get_db.get_db import get_db
from model.crud.base_crud import BaseCurd
from model.scheam.donation_scheam import Donation_scheam
from settings.verify_token.verify_token import get_token_header


class Donation_router(APIRouter):
    def __init__(self):
        super().__init__()
        common_dependencies = [Depends(get_token_header)]
        self.add_api_route("/list", self.donation_list, methods=["GET"], summary='打赏记录列表', dependencies=common_dependencies)
        self.add_api_route("/add", self.donation_add, methods=["POST"], summary='添加打赏记录', dependencies=common_dependencies)
        self.add_api_route("/change/{id}", self.donation_change, methods=["PUT"], summary='修改打赏记录', dependencies=common_dependencies)
        self.add_api_route("/delete/{id}", self.donation_remove, methods=["DELETE"], summary='删除打赏记录', dependencies=common_dependencies)

    async def donation_list(self, type_: int, auth_name: str = None, start_time: str = None, end_time: str = None, sort_by: str = 'create_time',sort_order: str = 'asc',current: int = 1,page_size: int = 20,db: Session = Depends(get_db),):
        # 搜索文章评论
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

        return await BaseCurd(db, Donation).query_(search_dict)

    async def donation_add(self, item: Donation_scheam, db: Session = Depends(get_db)):
        # 添加打赏记录
        return BaseCurd(db, Donation).create_({'curd': item.dict(), 'is_commit': True})

    async def donation_change(self, item: Donation_scheam, id: int, db: Session = Depends(get_db)):
        # 修改打赏记录
        return BaseCurd(db, Donation).update_({'query': {'id': id}, 'curd': item.dict(), 'is_commit': True})

    async def donation_remove(self, id: int, db: Session = Depends(get_db)):
        # 删除打赏记录
        return BaseCurd(db, Donation).update_({'query': {'id': id}, 'curd': {'status':0}, 'is_commit': True})


donation_router = Donation_router()