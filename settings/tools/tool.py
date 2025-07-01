import re
import uuid
import random
import secrets
from typing import Optional


class Check_re:
    TYPE_REGEX = {
        'email': r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}',
        'url': r'^((https|http|ftp|rtsp|mms)?://)[^\s]+',
        'phone': r'^1[3-9]\d{9}$',
        'id_card': r'^\d{15}|\d{17}[\dXx]$',
        'ip': r'^(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)'
              r'\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)'
              r'\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)'
              r'\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$'
    }

    def check_re(self, data: str, type_: str) -> Optional[str]:
        """正则表达式数据校验"""
        pattern = self.TYPE_REGEX.get(type_)
        if not pattern:
            raise ValueError(f"Unsupported type: {type_}")
        match = re.fullmatch(pattern, data)
        return match.group(0) if match else None


    def check_space(self, data):
        '''检查密码虹是否含有空格'''
        return ' ' not in data

    def code(self, alpha=True):
        s = ''  # 创建字符串变量,存储生成的验证码
        for i in range(6):  # 通过for循环控制验证码位数
            num = random.randint(0, 9)  # 生成随机数字0-9
            if alpha:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
                upper_alpha = chr(random.randint(65, 90))
                lower_alpha = chr(random.randint(97, 122))
                # 从列表中 [], 返回一个随机元素
                num = random.choice([num, upper_alpha, lower_alpha])
            s = s + str(num)
        return s


class Tools:
    def expand_detail_list(self, list: list) -> list:
        result = []
        for item in list:
            count = item.get('quantity', 1)
            time = item.get('time')
            for _ in range(count):
                result.append({
                    'time': time,
                    'quantity': 1,
                    'upper_switch': 1 if item['upper_screen'] else 0,
                    'collection_switch': 1 if item['collection'] else 0,
                })
        return result

    def generate_uuid(self):
        '''32位不重复的UUID，去掉-'''
        return uuid.uuid4().hex  # 相当于 str(uuid.uuid4()).replace("-", "")

    def ge_uuid(self):
        '''获取30位不重复的id字符串'''
        return secrets.token_hex(15)

    # def drop_tables(self, *models):
    #     tables = [model.__table__ for model in models]
    #     db.Base.metadata.drop_all(engine, tables=tables)
    #
    # def create_tables(self, *models):
    #     tables = [model.__table__ for model in models]
    #     db.Base.metadata.create_all(bind=engine, tables=tables)


check_re = Check_re()
tool_tool = Tools()