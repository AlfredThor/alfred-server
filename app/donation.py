from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from settings.get_db.get_db import get_db
from model.scheam.acticle_scheam import Article_scheam
from settings.verify_token.verify_token import get_token_header


class Donation_router(APIRouter):
    def __init__(self):
        super().__init__()
        common_dependencies = [Depends(get_token_header)]
        self.add_api_route("/list", self.donation_list, methods=["GET"], summary='打赏记录列表', dependencies=common_dependencies)
        self.add_api_route("/add", self.donation_add, methods=["POST"], summary='添加打赏记录', dependencies=common_dependencies)
        self.add_api_route("/change/{id}", self.donation_change, methods=["PUT"], summary='修改打赏记录', dependencies=common_dependencies)
        self.add_api_route("/delete/{id}", self.donation_remove, methods=["DELETE"], summary='删除打赏记录', dependencies=common_dependencies)

    async def donation_list(self, db: Session = Depends(get_db)):
        # 打赏记录列表
        pass

    async def donation_add(self, db: Session = Depends(get_db)):
        # 添加打赏记录
        pass

    async def donation_change(self, id: int, db: Session = Depends(get_db)):
        # 修改打赏记录
        pass

    async def donation_remove(self, id: int, db: Session = Depends(get_db)):
        # 删除打赏记录
        pass


donation_router = Donation_router()