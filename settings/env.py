import os


# =============================================== 配置 =================================================


# 应用根目录
FASTAPI_ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SERVER_SITE = os.getenv('SERVER_SITE', 'http://server.thornasa.com:7001')
JWT_KEY = os.getenv('JWT_KEY', '17610855585')


# =============================================== 数据库配置 =================================================


# 数据库驱动
PG_DRIVER = os.getenv('DB_DRIVER', 'postgres')
# 数据库地址
PG_HOST = os.getenv('DB_HOST', '47.106.35.207')
# 数据库端口
PG_PORT = os.getenv('DB_PORT', 5433)
# 数据库名称
PG_DATABASE = os.getenv('DB_DATABASE', 'article')
# 数据库账号
PG_USERNAME = os.getenv('DB_USERNAME', 'alfred')
# 数据库密码
PG_PASSWORD = os.getenv('DB_PASSWORD', 'Admin911$')
# MySQL数据库链接(当前使用的数据库)
PGSQL_URL = 'postgresql://' + PG_USERNAME + ':' + PG_PASSWORD + '@' + PG_HOST + ':' + str(PG_PORT) + '/' + PG_DATABASE + '?connect_timeout=10'


# =============================================== 缓存配置 =================================================


# 缓存服务地址
REDIS_HOST = os.getenv('REDIS_HOST', '113.45.177.139')
# 缓存服务端口
REDIS_PORT = os.getenv('REDIS_PORT', 6388)
# 缓存服务密码
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'aptx4869')
# 缓存库索引
REDIS_INDEX = os.getenv('REDIS_INDEX', 7)
# AUTH 为 True 时需要进行 用户认证
REDIS_AUTH = (os.getenv('REDIS_AUTH', 'True') == 'True')
# 是否对查询结果进行编码处理
REDIS_DECODE_RESPONSES = (os.getenv('REDIS_DECODE_RESPONSES', 'True') == 'True')


# =============================================== RabbitMQ配置 =================================================


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '47.106.35.207')
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', "Admin911$")
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
RABBITMQ_URL = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"
)