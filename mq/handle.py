# 你的消息处理逻辑（异步函数）
async def handle_message(msg: str):
    print(f"[x] Received: {msg}")
    # TODO: 处理业务逻辑，比如写数据库、发送通知等