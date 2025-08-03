from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from settings.get_db.get_db import get_db
from model.crud.base_crud import BaseCurd
from model.models.model import Monthes
from model.scheam.monehes_scheam import Monthes_auth_scheam
from settings.verify_token.verify_token import get_token_header


class Finance_router(APIRouter):
    def __init__(self):
        super().__init__()
        common_dependencies = [Depends(get_token_header)]
        self.add_api_route("/list", self.finance_list, methods=["GET"], summary='财务列表')
        self.add_api_route("/add", self.finance_add, methods=["POST"], summary='财务分类')
        self.add_api_route("/change/{id}", self.finance_change, methods=["PUT"], summary='修改财务')
        self.add_api_route("/delete/{id}", self.finance_remove, methods=["DELETE"], summary='删除财务')

    async def finance_list(self,type_: int, status: int, auth_name: str = None, start_time: str = None, end_time: str = None, sort_by: str = 'create_time',sort_order: str = 'asc',current: int = 1,page_size: int = 20,db: Session = Depends(get_db),):
        search_dict = {
            'curd': False,  # 搜索的字段
            'all_field': False,  # 是否返回所有字段
            'reverse': True,  # 是否反转
            'query_type': 'and',  # 搜索类型
            'export': ['password'],  # 反转的字段
            'group_sort': {
                'group_by': 'id',  # 是否分组
                'sort_by': sort_by,  # 排序字段
                'sort_order': sort_order,  # asc:生序/desc:降序
            },
            'is_first': True if type_ == 0 else False,  # 是否返回一条数据
            'pagination': {'current': current, 'page_size': page_size}  # 分页 current:第几页/page_size:每页多少数据
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

        return BaseCurd(db, Monthes).query_(search_dict)


    async def finance_add(self, items: Monthes_auth_scheam, db: Session = Depends(get_db)):
        # 添加客服
        print(items.dict())
        return BaseCurd(db, Monthes).create_({'curd': items.dict(),'is_commit': True})

    async def finance_change(self, id: int, db: Session = Depends(get_db)):
        # 修改客服
        pass

    async def finance_remove(self, id: int, db: Session = Depends(get_db)):
        # 删除客服
        pass


finance_router = Finance_router()