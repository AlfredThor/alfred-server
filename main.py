import asyncio
from app import *
from fastapi import FastAPI
from mq.handle import handle_message
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from mq.rabbitmq_consumer import RabbitMQConsumer
from fastapi.middleware.cors import CORSMiddleware


# ========= RabbitMQ 配置 =========


# 创建消费者实例
consumer = RabbitMQConsumer(queue_name="my_queue")


# ========= lifespan 生命周期处理器 =========

@asynccontextmanager
async def lifespan(app: FastAPI):
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
    allow_origins=[
        'http://localhost:5173',
        'http://localhost:15006',
        'http://localhost:15400',
        'https://www.hzmiguan.cn',
        'https://www.pahaigo.com',
    ],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
    expose_headers=["Content-Disposition"],
)


# 静态资源（需要时取消注释）
app.mount("/upload", StaticFiles(directory="upload"), name="upload")


# 注册路由
app.include_router(article_router, prefix='/article', tags=['文章'])


# ========= 启动 =========
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8002, reload=True)
