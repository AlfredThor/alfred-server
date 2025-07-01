from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from settings.get_db.get_db import get_db
from model.scheam.acticle_scheam import Article_scheam
from settings.verify_token.verify_token import get_token_header


class Article_router(APIRouter):
    def __init__(self):
        super().__init__()
        common_dependencies = [Depends(get_token_header)]
        self.add_api_route("/list", self.list, methods=["GET"], dependencies=common_dependencies)
        self.add_api_route("/add", self.add, methods=["POST"], dependencies=common_dependencies)
        self.add_api_route("/change/{id}", self.change, methods=["PUT"], dependencies=common_dependencies)
        self.add_api_route("/delete/{id}", self.remove, methods=["DELETE"], dependencies=common_dependencies)

    async def list(self, user_id: int, db: Session = Depends(get_db), token_data=Depends(get_token_header),):
        return {"msg": f"User ID: {user_id}"}

    async def add(self,items: Article_scheam):
        return {"msg": "User created", "data": items}

    async def change(self, id: int, items: Article_scheam):
        return {"msg": "User updated", "data": items, "id": id}

    async def remove(self, id: int):
        return {"msg": "User deleted", "data": id}


article_router = Article_router()