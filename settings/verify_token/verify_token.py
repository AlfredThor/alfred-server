import re
from fastapi import Depends
from settings.get_db.get_db import get_db
from sqlalchemy.orm import Session
# from tools.TokenSetting import permissions
from fastapi import Request, Header, HTTPException


async def get_token_header(request: Request, db: Session = Depends(get_db),  token: str = Header(None)):
    if not token:
        raise HTTPException(status_code=405, detail='Token为空,请先登陆!')

    uuid_pattern = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
    search_dict = {
        'db': db,
        'token': token,
        'path': re.sub(rf'/(?:{uuid_pattern}|\d+)$', '',  request.url.path)
    }

    # token_info = await permissions.query_userinfo(search_dict)
    #
    # search_dict['role_name'] = token_info['user_info']['role_name']
    # permissions.query_role(search_dict)

    return search_dict