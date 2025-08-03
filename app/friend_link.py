from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from settings.get_db.get_db import get_db
from model.scheam.acticle_scheam import Article_scheam
from settings.verify_token.verify_token import get_token_header


class Friend_link_router(APIRouter):
    def __init__(self):
        super().__init__()
        common_dependencies = [Depends(get_token_header)]
        self.add_api_route("/list", self. friend_link_list, methods=["GET"], summary='友情链接列表', dependencies=common_dependencies)
        self.add_api_route("/add", self. friend_link_add, methods=["POST"], summary='添加友情链接', dependencies=common_dependencies)
        self.add_api_route("/change/{id}", self. friend_link_change, methods=["PUT"], summary='修改友情链接', dependencies=common_dependencies)
        self.add_api_route("/delete/{id}", self. friend_link_remove, methods=["DELETE"], summary='删除友情链接', dependencies=common_dependencies)

    async def friend_link_list(self, db: Session = Depends(get_db)):
        # 友情链接列表
        pass

    async def friend_link_add(self, db: Session = Depends(get_db)):
        # 添加友情链接
        pass

    async def friend_link_change(self, id: int, db: Session = Depends(get_db)):
        # 修改友情链接
        pass

    async def friend_link_remove(self, id: int, db: Session = Depends(get_db)):
        # 删除友情链接
        pass


friend_link_router = Friend_link_router()