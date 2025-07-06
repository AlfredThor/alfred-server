import asyncio
from app import *
from fastapi import FastAPI
from model.models import model
from sqlalchemy import inspect
from mq.handle import handle_message
from config.config import Base, engine
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from mq.rabbitmq_consumer import RabbitMQConsumer
from fastapi.middleware.cors import CORSMiddleware


# ========= RabbitMQ 配置 =========


# 创建消费者实例
consumer = RabbitMQConsumer(queue_name="my_queue")


# ========= 创建数据表实例 =========
def create_db():
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    print("🔍 已加载模型表:", [t.name for t in Base.metadata.sorted_tables])

    for table in Base.metadata.sorted_tables:
        if table.name not in existing_tables:
            print(f"✅ 创建表：{table.name}")
        else:
            print(f"⏩ 跳过已有表：{table.name}")

    Base.metadata.create_all(bind=engine)


# ========= lifespan 生命周期处理器 =========
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ 启动前，创建数据库表（如果不存在）
    create_db()
    # 启动前
    asyncio.create_task(consumer.consume(handle_message))
    print("🐇 RabbitMQ consumer started (via lifespan)")
    yield
    # 关闭时（可选）
    await consumer.close()
    print("🔌 RabbitMQ consumer closed.")


# ========= 创建 app 实例 =========
app = FastAPI(lifespan=lifespan)


# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
    expose_headers=["Content-Disposition"],
)


# 静态资源（需要时取消注释）
app.mount("/upload", StaticFiles(directory="upload"), name="upload")


# 注册路由
app.include_router(article_router, prefix='/article', tags=['文章'])
app.include_router(category_router, prefix='/category', tags=['文章分类'])
app.include_router(tag_router, prefix='/tag', tags=['文章标签'])
app.include_router(comment_router, prefix='/comment', tags=['文章评论'])
app.include_router(friend_link_router, prefix='/friend/links', tags=['友链'])
app.include_router(visit_log_router, prefix='/logger', tags=['日志'])
app.include_router(donation_router, prefix='/donation', tags=['打赏'])


# ========= 启动 =========
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8002, reload=True)