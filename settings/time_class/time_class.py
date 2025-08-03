from datetime import datetime, timedelta


class TimeClass:
    def __init__(self):
        self.now_time = datetime.now()

    def get_year(self):
        return self.now_time.year

    def get_month(self):
        return self.now_time.month

    def get_day(self):
        return self.now_time.day

    def get_three_day(self):
        now = datetime.now()
        three_days_later = now + timedelta(days = 3)
        return three_days_later.strftime("%Y-%m-%d %H:%M:%S")

    def in_time(self, info, lists):
        '''将时间转换成时间戳'''
        if isinstance(info, dict):
            for key, value in info.items():
                if key in lists:
                    value = str(value).replace("Z", "")
                    info[key] = int(datetime.fromisoformat(str(value)).timestamp()*1000)

            return info

        if isinstance(info, list):
            for i in info:
                for key, value in i.items():
                    if key in lists:
                        value = str(value).replace("Z", "")
                        i[key] = int(datetime.fromisoformat(value).timestamp()*1000)
            return info

    def convert_times_to_timestamp(self, data):
        def clean_and_convert_time(record: dict):
            # 处理时间字段
            time_val = record.get('time')
            if isinstance(time_val, str) and time_val:
                try:
                    record['time'] = int(datetime.fromisoformat(
                        time_val.replace('Z', '+00:00')
                    ).timestamp() * 1000)
                except Exception as e:
                    # 遇到无效字符串，选择删除该字段
                    record.pop('time', None)

            # 清理所有空字符串或 None 的字段（注意保留 0）
            return {k: v for k, v in record.items() if v not in ['', None]}

        for parent in data:
            # 处理父节点
            cleaned_parent = clean_and_convert_time(parent)

            # 处理子节点
            children = parent.get('children', [])
            cleaned_children = [clean_and_convert_time(child) for child in children if isinstance(child, dict)]

            # 更新结构
            parent.clear()
            parent.update(cleaned_parent)
            if cleaned_children:
                parent['children'] = cleaned_children

        return data



time_class = TimeClass()