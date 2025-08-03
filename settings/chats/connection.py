import json
from model.crud.base_crud import BaseCurd
from settings.get_db.get_db import get_db
from model.models.model import ChatMessage
from fastapi import WebSocket, WebSocketDisconnect


# 聊天管理器
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        '''接受连接请求'''
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        '''移除一个请求'''
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        '''广播消息'''
        for connection in self.active_connections:
            await connection.send_text(message)


class ChatController:
    def __init__(self):
        self.manager = ConnectionManager()

    async def handle_chat(self, websocket: WebSocket):
        await self.manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                data_info = json.loads(data)
                BaseCurd(next(get_db()), ChatMessage).create_({
                    'curd': {'room_id':1,'username':data_info['nickname'],'content':data_info['content'],'create_time':data_info['create_time'],'msg_type':'text'},
                    'is_commit': True
                })
                await self.manager.broadcast(f"{data}")

        except WebSocketDisconnect:
            self.manager.disconnect(websocket)
            await self.manager.broadcast("有用戶離線")