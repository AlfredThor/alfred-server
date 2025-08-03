from celery_app import celery_app  # 上面的 celery_app 实例

class Delete_files:

    @staticmethod
    @celery_app.task(name="delete_file")
    def delete_file(user_id: int, amount: float):
        print(f"🎁 用户 {user_id} 打赏了 {amount}")