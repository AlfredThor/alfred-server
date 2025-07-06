from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from settings.get_db.get_db import get_db
from model.scheam.acticle_scheam import Article_scheam
from settings.verify_token.verify_token import get_token_header


class Visit_log_router(APIRouter):
    def __init__(self):
        super().__init__()
        common_dependencies = [Depends(get_token_header)]
        self.add_api_route("/list", self.visit_log_list, methods=["GET"], summary='日志列表', dependencies=common_dependencies)
        self.add_api_route("/add", self.visit_log_add, methods=["POST"], summary='添加日志', dependencies=common_dependencies)
        self.add_api_route("/change/{id}", self.visit_log_change, methods=["PUT"], summary='修改日志', dependencies=common_dependencies)
        self.add_api_route("/delete/{id}", self.visit_log_remove, methods=["DELETE"], summary='删除日志', dependencies=common_dependencies)

    async def  visit_log_list(self, db: Session = Depends(get_db)):
        # 日志列表
        pass

    async def  visit_log_add(self, db: Session = Depends(get_db)):
        # 添加日志
        pass

    async def  visit_log_change(self, id: int, db: Session = Depends(get_db)):
        # 修改日志
        pass

    async def  visit_log_remove(self, id: int, db: Session = Depends(get_db)):
        # 删除日志
        pass


visit_log_router = Visit_log_router()