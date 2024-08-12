import requests
from loguru import logger


class ServiceBase:
    """
    服务基类
    """

    def notify_cannot_get_file_from_url(self, url: str, notify_url: str, task_id: str) -> None:
        """
        找不到指定的文件
        :param url:
        :param notify_url:
        :param task_id:
        :return:
        """
        try:
            post_data = {"task_id": task_id, "result": "", "success": False,
                         "message": "从指定的url下载文件失败"}
            requests.post(notify_url, json=post_data)
            logger.warning(f"回调结果：成功；回调原因：从指定的url下载文件失败，task_id：{task_id}, url: {url}")
        except Exception as e:
            logger.error(f"回调请求失败，task_id: {task_id}，详细信息：{str(e)}")

    def notify_cannot_parse_file_content(self, url: str, notify_url: str, task_id: str) -> None:
        try:
            post_data = {"task_id": task_id, "result": "", "success": False,
                         "message": "解析文件内容失败"}
            requests.post(notify_url, json=post_data)
            logger.warning(f"回调结果：成功；回调原因：解析文件内容失败，task_id：{task_id}, url: {url}")
        except Exception as e:
            logger.error(f"回调请求失败，task_id: {task_id}，详细信息：{str(e)}")

    def notify_bad_request(self, url: str, notify_url: str, task_id: str, error_message: str) -> None:
        """
        通知错误（自定义错误消息）
        :param url:
        :param notify_url:
        :param task_id:
        :param error_message:
        :return:
        """
        try:
            post_data = {"task_id": task_id, "result": "", "success": False,
                         "message": error_message}
            requests.post(notify_url, json=post_data)
            logger.warning(f"回调结果：成功；回调原因：请求错误（{error_message}），task_id：{task_id}, url: {url}")
        except Exception as e:
            logger.error(f"回调请求失败，task_id: {task_id}，详细信息：{str(e)}")

    def notify_fail_by_self_error(self, url: str, notify_url: str, task_id: str) -> None:
        """
        服务出错时的回调
        :param url:
        :param notify_url:
        :param task_id:
        :return:
        """
        try:
            post_data = {"task_id": task_id, "result": "", "success": False,
                         "message": "处理请求的内容失败"}
            response = requests.post(notify_url, json=post_data)
            logger.warning(f"回调结果：成功；回调原因：处理请求的内容失败，task_id：{task_id}, url: {url}")
        except Exception as e:
            logger.error(f"回调请求失败，task_id: {task_id}，详细信息：{str(e)}")

    def notify_success_with_data(self, notify_url: str, task_id: str, data: str) -> None:
        """
        回调成功
        :param notify_url:
        :param task_id:
        :param data:
        :return:
        """
        try:
            post_data = {"task_id": task_id, "result": data, "success": True, "message": "成功"}
            response = requests.post(notify_url, json=post_data)
            logger.info(f"回调结果成功，task_id：{task_id}, 状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"回调请求失败，task_id: {task_id}，详细信息：{str(e)}")
