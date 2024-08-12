from api.model import PdfData, ExtractedInfo
from api.utility import UieHelper
import requests
import os
import time
from loguru import logger
from api.utility import HttpUtils
from api.services.ServiceBase import ServiceBase


class InfoExtractionService(ServiceBase):
    """
    信息提取服务
    """

    def __init__(self):

        pass

    def get_json_from_url(self, url):
        """
        获取指定URL的内容
        :return:
        """
        try:
            # 发送GET请求到指定的URL
            response = requests.get(url)

            # 检查请求是否成功
            if response.status_code == 200:
                # 将JSON内容解析为Python对象
                json_data = response.content.decode(encoding="utf-8")
                return json_data, None
            else:
                return None, f"请求失败。状态码: {response.status_code}"
        except requests.RequestException as e:
            return None, f"请求出错: {str(e)}"

    def process(self, schema, url: str, notify_url: str, task_id: str) -> None:
        """
        信息提取
        :param schema: 要提取的内容
        :param url: 待提取的文件URL
        :param notify_url: 提取完成后要通知的URL
        :param task_id: 任务ID
        :return: 无返回
        """

        # 先从本地获取文件
        uie_helper = UieHelper.get_instance()
        uie_helper.set_schema(schema)

        data = HttpUtils.get_json_from_url(url)
        if data[0] is None:
            # 下载文件失败
            super().notify_cannot_get_file_from_url(url, notify_url, task_id)
            return

        pdf_data = PdfData.deserialize_from_json(data[0])

        extract_result = {}
        for index, content in pdf_data.data.items():
            page_result = uie_helper.extract(content)
            logger.info(page_result)
            if len(page_result) == 1 and len(page_result[0]) == 0:  # 空字典
                continue
            extract_result[index] = page_result

        # logger.info(extract_result)

        # 回调
        try:
            post_data = {"task_id": task_id, "result": extract_result, "success": True,
                         "message": ""}
            response = requests.post(notify_url, json=post_data)
            logger.info(f"回调结果成功，task_id：{task_id}, 状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"回调请求失败，task_id: {task_id}，详细信息：{str(e)}")

    def extract_info_from_json(self, items):
        json_dir = "./data"
        target_json_dir = "./extracted"
        # 使用os.listdir获取目录中的所有文件和目录名
        files = [os.path.join(json_dir, file) for file in os.listdir(json_dir) if
                 os.path.isfile(os.path.join(json_dir, file)) and "_extracted" not in file]
        start_time = time.time()  # 开始时间

        uie_helper = UieHelper(items)
        for file in files:

            extracted_info = ExtractedInfo()
            extracted_info.file_path = file
            extracted_info.data = {}
            pdata = PdfData.deserialize_from_file(file)
            for index, content in pdata.data.items():
                print(content)
                if len(content) == 0:
                    continue
                info = uie_helper.extract(content)
                if len(info) == 0:
                    continue
                extracted_info.data[index] = info

            file_name = os.path.basename(file)
            target_json_path = f"{target_json_dir}/{file_name}"
            extracted_info.serialize_to_json(target_json_path)
