from api.utility import HttpUtils
import json
from api.model import DocRoot
from api.services.ServiceBase import ServiceBase
from api.services.TechStandardIdentifyService import TechStandardIdentifyService
from api.app_const import InvalidContentType


class InvalidContentIdentifyService(ServiceBase):
    """
    无效内容识别服务
    """

    def process_sync(self, url: str, notify_url: str, task_id: str, options: []):
        # 去重
        final_options = set(options)
        # 判断options中至少有一个有效的检查项
        if not final_options & set(InvalidContentType.get_all_values()):
            return None, "未指定有效的检查项"

        data = HttpUtils.get_json_from_url(url)
        if data[0] is None:
            # 下载文件失败
            return None, "从指定的url下载文件失败"

        is_valid_json: bool = True
        original_doc_root: DocRoot = None
        try:
            # 解析文件
            json_data = json.loads(data[0])
            original_doc_root = DocRoot.parse_json_to_dataclasses(json_data)  # 原始标书数据
        except Exception:
            # 解析文件失败
            is_valid_json = False

        if not is_valid_json or original_doc_root is None:
            return None, "解析文件内容失败"

        # 通过预检查（文件下载与解析），开始逐项进行检查
        result_dict = {}
        for option in final_options:
            if option == InvalidContentType.TECH_STANDARD.value:
                tech_standard_identify = TechStandardIdentifyService()
                ts_result, ts_message = tech_standard_identify.identify(original_doc_root)
                if ts_result is not None:
                    result_dict[option] = DocRoot.serialize(ts_result)
            elif option == InvalidContentType.TABLE_OF_CONTENT.value:
                tech_standard_identify = TechStandardIdentifyService()
                ts_result, ts_message = tech_standard_identify.identify(original_doc_root)
                if ts_result is not None:
                    result_dict[option] = DocRoot.serialize(ts_result)

        return result_dict, None

    def process(self, url: str, notify_url: str, task_id: str, options: []) -> None:
        """
        处理（调用相应的服务）
        :param url:
        :param notify_url:
        :param task_id:
        :param options:
        :return:
        """

        # 去重
        final_options = set(options)
        # 判断options中至少有一个有效的检查项
        if not final_options & set(InvalidContentType.get_all_values()):
            super().notify_bad_request(url, notify_url, task_id, error_message="未指定有效的检查项")
            return

        data = HttpUtils.get_json_from_url(url)
        if data[0] is None:
            # 下载文件失败
            super().notify_cannot_get_file_from_url(url, notify_url, task_id)
            return

        is_valid_json: bool = True
        original_doc_root: DocRoot = None
        try:
            # 解析文件
            json_data = json.loads(data[0])
            original_doc_root = DocRoot.parse_json_to_dataclasses(json_data)  # 原始标书数据
        except Exception:
            # 解析文件失败
            is_valid_json = False

        if not is_valid_json or original_doc_root is None:
            super().notify_cannot_parse_file_content(url, notify_url, task_id)
            return

        # 通过预检查（文件下载与解析），开始逐项进行检查
        result_dict = {}
        for option in final_options:
            if option == InvalidContentType.TECH_STANDARD.value:
                tech_standard_identify = TechStandardIdentifyService()
                ts_result, ts_message = tech_standard_identify.identify(original_doc_root)
                if ts_result is not None:
                    result_dict[option] = DocRoot.serialize(ts_result)
            elif option == InvalidContentType.TABLE_OF_CONTENT.value:
                tech_standard_identify = TechStandardIdentifyService()
                ts_result, ts_message = tech_standard_identify.identify(original_doc_root)
                if ts_result is not None:
                    result_dict[option] = DocRoot.serialize(ts_result)

        super().notify_success_with_data(notify_url, task_id, result_dict)
