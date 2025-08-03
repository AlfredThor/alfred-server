import os
import uuid
import shutil
from settings.time_class.time_class import time_class
from settings.env import FASTAPI_ROOT_PATH
from fastapi.responses import FileResponse
from fastapi import HTTPException, Depends, APIRouter
from fastapi import UploadFile, Form, File, Response


class File_router(APIRouter):
    def __init__(self):
        super().__init__()
        self.add_api_route('/img/upload', self.upload_img, summary='付款截图上传', methods=['POST'])

    async def upload_img(self, file: UploadFile = File(...)):
        # 获取文件扩展名
        ext = file.filename.split(".")[-1].lower()
        if ext not in ["jpg", "jpeg", "png", "gif"]:
            raise HTTPException(status_code=400, detail="不支持的文件类型")
            # return {}

        file_location = '/upload/{}/{}/{}/'.format(
            time_class.get_year(),
            time_class.get_month(),
            time_class.get_day(),
        )

        # 生成唯一文件名
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        file_path = os.path.join(file_location, filename)

        if not os.path.exists(FASTAPI_ROOT_PATH + file_location):
            os.makedirs(FASTAPI_ROOT_PATH + file_location)

        # 保存文件
        with open(FASTAPI_ROOT_PATH + file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # 本地
        # http_location = 'http://127.0.0.1:8002' + file_path
        # 测试
        http_location = 'https://houduan.pahaigo.com:7001' + file_path
        # 返回文件访问地址
        return {'code': 200, 'message': '上传成功！', 'info': [http_location]}


file_router = File_router()