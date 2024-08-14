import joblib
from api.model import DocRoot, DocumentGroup, Document
from loguru import logger
from numpy import ndarray
from api.services.ServiceBase import ServiceBase
import os
from typing import Optional, Tuple


class TOCIdentifyService(ServiceBase):
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TOCIdentifyService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        logger.info("实例化TechStandardIdentifyService")
        if not self._is_initialized:
            self._load_model()
            TOCIdentifyService._is_initialized = True

    def _load_model(self) -> None:
        """
        加载模型与分词
        :return:
        """

        try:
            # 加载模型
            logger.info(f"当前目录： {os.getcwd()}")
            prefix = "../" if os.getcwd().endswith("api") else ""
            self.model = joblib.load(prefix + 'training/saved_models/toc_model.joblib')
            # 加载vectorizer
            self.vectorizer = joblib.load(prefix + 'training/saved_models/toc_vectorizer.joblib')
        except Exception as e:
            logger.exception(e)

    def predict(self, content: str):
        content_vectored = self.vectorizer.transform(content)
        return self.model.predict(content_vectored)

    def identify(self, original_doc_root: DocRoot) -> Tuple[Optional[DocRoot], Optional[str]]:
        """
        目录识别
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
            return None, f"目录识别出现异常: {str(e)}"

        return target_doc_root, None
