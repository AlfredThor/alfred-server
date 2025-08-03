from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from settings.get_db.get_db import get_db
from model.scheam.acticle_scheam import Article_scheam
from settings.verify_token.verify_token import get_token_header


class Tag_router(APIRouter):
    def __init__(self):
        super().__init__()
        common_dependencies = [Depends(get_token_header)]
        self.add_api_route("/list", self.tag_list, methods=["GET"], summary='标签列表', dependencies=common_dependencies)
        self.add_api_route("/add", self.tag_add, methods=["POST"], summary='添加标签', dependencies=common_dependencies)
        self.add_api_route("/change/{id}", self.tag_change, methods=["PUT"], summary='修改标签', dependencies=common_dependencies)
        self.add_api_route("/delete/{id}", self.tag_remove, methods=["DELETE"], summary='删除标签', dependencies=common_dependencies)

    async def tag_list(self, db: Session = Depends(get_db)):
        # 标签列表
        pass

    async def tag_add(self, db: Session = Depends(get_db)):
        # 标签分类
        pass

    async def tag_change(self, id: int, db: Session = Depends(get_db)):
        # 标签分类
        pass

    async def tag_remove(self, id: int, db: Session = Depends(get_db)):
        # 标签分类
        pass


tag_router = Tag_router()