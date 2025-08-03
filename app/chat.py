from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.sql.functions import current_date
from model.crud.base_crud import BaseCurd
from model.models.model import ChatMessage
from settings.get_db.get_db import get_db
from settings.chats.connection import ChatController


class ChatRouter:
    def __init__(self):
        self.controller = ChatController()
        self.router = APIRouter()
        self.router.add_api_websocket_route("/ws", self.chat_endpoint)
        self.router.add_api_route("/list", self.chat_list)

    async def chat_endpoint(self, websocket: WebSocket):

        await self.controller.handle_chat(websocket)

    async def chat_list(self, username: str = None, start_time: str = None, end_time: str = None, current: int = 1, page_size: int = 20, sort_by: str = 'create_time', sort_order: str = 'desc', db: Session = Depends(get_db)):
        search_dict = {
            'curd': False,  # 搜索的字段
            'all_field': False,  # 是否返回所有字段
            'reverse': False,  # True 显示不在export中的字段/False 显示在export中的字段
            'query_type': 'and',  # 搜索类型
            'export': ['username','content','create_time'],  # 反转的字段
            'group_sort': {
                'group_by': 'id',  # 是否分组
                'sort_by': sort_by,  # 排序字段
                'sort_order': sort_order,  # asc:生序/desc:降序
            },
            'is_first': False,  # 是否返回一条数据
            'pagination': {'current': current, 'page_size': page_size},  # 分页 current:第几页/page_size:每页多少数据
            # "aggregates": {
            #     "sum": ["product_amount", 'task_id'],  # 某一列的总和
                # "avg": func.avg,  # 平均值
                # "max": func.max,  # 最大
                # "min": func.min,  # 最小
                # "count": func.count  # 数量
            # }
        }
        curd = {}
        if username:
            curd['username'] = username
        if start_time:
            curd['start_time'] = start_time
        if end_time:
            curd['end_time'] = end_time

        if len(curd) >= 1:
            search_dict['curd'] = curd

        return BaseCurd(db, ChatMessage).query_(search_dict)


chat_router = ChatRouter()  # 導出實際 router 給主程序掛載