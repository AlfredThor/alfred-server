from celery_app import celery_app  # 上面的 celery_app 实例

class FilesTasks:

    @staticmethod
    @celery_app.task(name="user.send_email")
    def delete_files(file_path: str):
        print(f"📧 正在发送邮件给：{file_path}")

    @staticmethod
    @celery_app.task(name="user.reward")
    def reward(user_id: int, amount: float):
        print(f"🎁 用户 {user_id} 打赏了 {amount}")
