"""
异步任务处理器
用于处理长时间运行的工作流任务
"""
import threading
import uuid
import time
from typing import Dict, Optional
import requests
import logging

logger = logging.getLogger(__name__)

# 任务状态存储（生产环境应使用Redis等）
tasks: Dict[str, dict] = {}

class AsyncTask:
    """异步任务类"""

    def __init__(self, task_id: str, coze_api_url: str, coze_api_token: str, input_data: dict):
        self.task_id = task_id
        self.coze_api_url = coze_api_url
        self.coze_api_token = coze_api_token
        self.input_data = input_data
        self.status = "pending"
        self.result = None
        self.error = None
        self.created_at = time.time()
        self.started_at = None
        self.completed_at = None

    def run(self):
        """执行任务"""
        try:
            self.status = "running"
            self.started_at = time.time()
            logger.info(f"任务 {self.task_id} 开始执行")

            # 调用Coze API
            headers = {
                'Authorization': f'Bearer {self.coze_api_token}',
                'Content-Type': 'application/json'
            }

            response = requests.post(
                self.coze_api_url,
                json=self.input_data,
                headers=headers,
                timeout=(60, 1200)  # 20分钟超时
            )

            if response.status_code == 200:
                self.result = response.json()
                self.status = "completed"
                logger.info(f"任务 {self.task_id} 执行成功")
            else:
                self.error = f"Coze API错误: {response.status_code}"
                self.status = "failed"
                logger.error(f"任务 {self.task_id} 执行失败: {self.error}")

        except requests.exceptions.Timeout:
            self.error = "请求超时（超过20分钟）"
            self.status = "failed"
            logger.error(f"任务 {self.task_id} 超时")
        except Exception as e:
            self.error = str(e)
            self.status = "failed"
            logger.error(f"任务 {self.task_id} 异常: {self.error}")
        finally:
            self.completed_at = time.time()
            logger.info(f"任务 {self.task_id} 完成，状态: {self.status}")

    def to_dict(self):
        """转换为字典"""
        duration = None
        if self.started_at and self.completed_at:
            duration = self.completed_at - self.started_at
        elif self.started_at:
            duration = time.time() - self.started_at

        return {
            'task_id': self.task_id,
            'status': self.status,
            'result': self.result if self.status == 'completed' else None,
            'error': self.error if self.status == 'failed' else None,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'duration': duration
        }


def create_task(coze_api_url: str, coze_api_token: str, input_data: dict) -> str:
    """创建异步任务"""
    task_id = str(uuid.uuid4())
    task = AsyncTask(task_id, coze_api_url, coze_api_token, input_data)
    tasks[task_id] = task

    # 在后台线程中运行任务
    thread = threading.Thread(target=task.run)
    thread.daemon = True
    thread.start()

    logger.info(f"任务 {task_id} 已创建，开始后台执行")
    return task_id


def get_task_status(task_id: str) -> Optional[dict]:
    """获取任务状态"""
    if task_id not in tasks:
        return None
    return tasks[task_id].to_dict()


def cleanup_old_tasks(max_age_seconds: int = 3600):
    """清理旧任务（1小时前）"""
    current_time = time.time()
    to_delete = []

    for task_id, task in tasks.items():
        if task.completed_at and (current_time - task.completed_at) > max_age_seconds:
            to_delete.append(task_id)

    for task_id in to_delete:
        del tasks[task_id]
        logger.info(f"清理旧任务: {task_id}")

    return len(to_delete)
