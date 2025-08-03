from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from settings.get_db.get_db import get_db
from model.scheam.acticle_scheam import Article_scheam
from settings.verify_token.verify_token import get_token_header


class Category_router(APIRouter):
    def __init__(self):
        super().__init__()
        common_dependencies = [Depends(get_token_header)]
        self.add_api_route("/list", self.category_list, methods=["GET"], summary='分类列表', dependencies=common_dependencies)
        self.add_api_route("/add", self.category_add, methods=["POST"], summary='添加分类', dependencies=common_dependencies)
        self.add_api_route("/change/{id}", self.category_change, methods=["PUT"], summary='修改分类', dependencies=common_dependencies)
        self.add_api_route("/delete/{id}", self.category_remove, methods=["DELETE"], summary='删除分类', dependencies=common_dependencies)

    async def category_list(self, db: Session = Depends(get_db)):
        # 分类列表
        pass

    async def category_add(self, db: Session = Depends(get_db)):
        # 添加分类
        pass

    async def category_change(self, id: int, db: Session = Depends(get_db)):
        # 修改分类
        pass

    async def category_remove(self, id: int, db: Session = Depends(get_db)):
        # 删除分类
        pass


category_router = Category_router()