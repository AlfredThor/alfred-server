from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from settings.get_db.get_db import get_db
from model.scheam.acticle_scheam import Article_scheam
from settings.verify_token.verify_token import get_token_header


class Comment_router(APIRouter):
    def __init__(self):
        super().__init__()
        common_dependencies = [Depends(get_token_header)]
        self.add_api_route("/list", self.comment_list, methods=["GET"], summary='文章评论列表', dependencies=common_dependencies)
        self.add_api_route("/add", self.comment_add, methods=["POST"], summary='添加文章评论', dependencies=common_dependencies)
        self.add_api_route("/change/{id}", self.comment_change, methods=["PUT"], summary='修改文章评论', dependencies=common_dependencies)
        self.add_api_route("/delete/{id}", self.comment_remove, methods=["DELETE"], summary='删除文章评论', dependencies=common_dependencies)

    async def comment_list(self, db: Session = Depends(get_db)):
        # 文章评论列表
        pass

    async def comment_add(self, db: Session = Depends(get_db)):
        # 添加文章评论
        pass

    async def comment_change(self, id: int, db: Session = Depends(get_db)):
        # 修改文章评论
        pass

    async def comment_remove(self, id: int, db: Session = Depends(get_db)):
        # 删除文章评论
        pass


comment_router = Comment_router()