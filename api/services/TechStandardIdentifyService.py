import joblib
from api.model import DocRoot, DocumentGroup, Document
from loguru import logger
from numpy import ndarray
from api.services.ServiceBase import ServiceBase
from typing import Optional, Tuple
import os


class TechStandardIdentifyService(ServiceBase):
    """
    技术标准提取服务
    """
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TechStandardIdentifyService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        logger.info("实例化TechStandardIdentifyService")
        if not self._is_initialized:
            self._load_model()
            TechStandardIdentifyService._is_initialized = True

    def _load_model(self) -> None:
        """
        加载模型与分词
        :return:
        """

        try:
            # 加载模型
            logger.info(f"当前目录： {os.getcwd()}")
            prefix = "../" if os.getcwd().endswith("api") else ""
            self.model = joblib.load(prefix + '/training/saved_models/tech_standard_model.joblib')
            # 加载vectorizer
            self.vectorizer = joblib.load(prefix + '/training/saved_models/tech_standard_vectorizer.joblib')
        except Exception as e:
            logger.exception(e)

    @property
    def get_model(self):
        return self.model

    @property
    def get_vectorizer(self):
        return self.vectorizer

    def predict(self, content: str):
        content_vectored = self.vectorizer.transform(content)
        return self.model.predict(content_vectored)

    def identify(self, original_doc_root: DocRoot) -> Tuple[Optional[DocRoot], Optional[str]]:
        """
        技术标准识别
        :param original_doc_root:
        :return:
        """
        target_doc_root = DocRoot(document_groups={})  # 检查结果
        try:
            for group_key, group_data in original_doc_root.document_groups.items():
                # 方案组
                target_doc_group_data = DocumentGroup(documents={})
                for doc_key, doc_data in group_data.documents.items():
                    # 文档
                    target_doc_data = Document(paragraphs=[])
                    # 将原文档中的段落转化为字符串列表以准备检查
                    doc_paragraphs: list[str] = [para.text for para in doc_data.paragraphs]
                    # 文本转为向量
                    para_vectors = self.vectorizer.transform(doc_paragraphs)
                    # 使用模型预测
                    doc_check_result: ndarray = self.model.predict(para_vectors)
                    for index, value in enumerate(doc_check_result):
                        if value == 1:
                            # 往结果对象中添加原文档中的段落
                            target_doc_data.paragraphs.append(doc_data.paragraphs[index])
                    # 当前文档已检查完，向方案组中添加当前文档的检查结果
                    target_doc_group_data.documents[doc_key] = target_doc_data
                # 添加方案组
                target_doc_root.document_groups[group_key] = target_doc_group_data
        except Exception as e:
            logger.exception(e)
            return None, f"技术标准识别出现异常: {str(e)}"

        return target_doc_root, None

    # def process(self, url: str, notify_url: str, task_id: str) -> None:
    #     """
    #     识别技术标准
    #     :param url: 标书解析后的JSON文件URL
    #     :param notify_url: 回调URL
    #     :param task_id: 任务ID
    #     :return:
    #     """
    #     data = HttpUtils.get_json_from_url(url)
    #     if data[0] is None:
    #         # 下载文件失败
    #         super().notify_cannot_get_file_from_url(url, notify_url, task_id)
    #         return
    #
    #     is_valid_json: bool = True
    #     original_doc_root: DocRoot = None
    #     try:
    #         # 解析文件
    #         json_data = json.loads(data[0])
    #         original_doc_root = DocRoot.parse_json_to_dataclasses(json_data)  # 原始标书数据
    #     except Exception:
    #         # 解析文件失败
    #         is_valid_json = False
    #
    #     if not is_valid_json or original_doc_root is None:
    #         super().notify_cannot_parse_file_content(url, notify_url, task_id)
    #         return
    #
    #     target_doc_root = DocRoot(document_groups={})  # 检查结果
    #     try:
    #         for group_key, group_data in original_doc_root.document_groups.items():
    #             # 方案组
    #             target_doc_group_data = DocumentGroup(documents={})
    #             for doc_key, doc_data in group_data.documents.items():
    #                 # 文档
    #                 target_doc_data = Document(paragraphs=[])
    #                 # 将原文档中的段落转化为字符串列表以准备检查
    #                 doc_paragraphs: list[str] = [para.text for para in doc_data.paragraphs]
    #                 # 文本转为向量
    #                 para_vectors = self.vectorizer.transform(doc_paragraphs)
    #                 # 使用模型预测
    #                 doc_check_result: ndarray = self.model.predict(para_vectors)
    #                 for index, value in enumerate(doc_check_result):
    #                     if value == 1:
    #                         # 往结果对象中添加原文档中的段落
    #                         target_doc_data.paragraphs.append(doc_data.paragraphs[index])
    #                 # 当前文档已检查完，向方案组中添加当前文档的检查结果
    #                 target_doc_group_data.documents[doc_key] = target_doc_data
    #             # 添加方案组
    #             target_doc_root.document_groups[group_key] = target_doc_group_data
    #     except Exception as e:
    #         logger.exception(e)
    #         super().notify_fail_by_self_error(url, notify_url, task_id)
    #         return
    #
    #     # 检查完成，回调请求
    #     super().notify_success_with_data(notify_url, task_id, target_doc_root.to_json())
