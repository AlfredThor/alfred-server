import jwt
import datetime
from settings.env import JWT_KEY
from settings.logger.logger import logger
# from model.model import Role, Auth
# from model.base_curd import BaseCurd
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret = JWT_KEY

    # 密码加密
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    # 密码校验
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    # token生成
    def encode_token(self, user_id, user_status, minutes=10080):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=minutes), # 超时时间
            'iat': datetime.utcnow(),
            'uuid': user_id,
            'user_status': user_status,
        }
        return str(jwt.encode(payload, self.secret, algorithm='HS256'))

    # token 解码
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return {'code':200, 'uuid': payload['uuid'], 'user_status': payload['user_status']}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=400, detail='Token已经超期，请重新登录！')
        except jwt.InvalidTokenError as error:
            logger.error(f'Token解码出错! token: {token} 报错信息: {error}')
            raise HTTPException(status_code=400, detail='非法的token！请重新登陆!')

    def auth_wrapper(self, oauth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(oauth.credentials)

    async def query_userinfo(self, dict):
        # 校验Token
        check_token = permissions.decode_token(dict['token'])

        # 用户信息
        user_info = BaseCurd(dict['db'], Auth).query_({
            'curd': {'uuid': check_token['uuid']},
            'all_field': False,
            'reverse': True,
            'export': ['password', 'create_time','update_time'],
            'query_type': 'and',
            'group_sort':False,
            'is_first': True
        })

        if user_info['code'] != 200:
            raise HTTPException(status_code=405, detail='Token校验出错！' + user_info['message'])

        if user_info['info']['status'] == 1:
            raise HTTPException(status_code=405, detail='帐户遭到封禁！')

        return {'code': 200, 'user_info': user_info['info'], 'token_info': check_token}

    def query_role(self, dict):
        # 检查角色是否有权限
        user_role = BaseCurd(dict['db'], Role).query_({
            'curd': {'role_name': dict['role_name'], 'status': 1},
            'query_type': 'and',
            'is_first': True,
            'all_field': False,
            'reverse': True,
            'group_sort': False,
            'export': ['create_time', 'update_time'],
        })

        if user_role['code'] == 404:
            raise HTTPException(status_code=405, detail='没有搜索到权限')

        if user_role['code'] == 200:
            try:
                if dict['path'] not in user_role['info']['role_authority']:
                    raise HTTPException(status_code=405, detail='没有访问权限')

            except Exception as error:
                logger.error('Token检查权限出错! 模型: {} 报错信息: {}'.format(dict['path'], error))
                raise HTTPException(status_code=405, detail='权限出错')


permissions = AuthHandler()