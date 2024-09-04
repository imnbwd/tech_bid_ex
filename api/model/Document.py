from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json
import uuid
from loguru import logger


@dataclass
class Paragraph:
    id: str
    page: str
    text: str

    def to_dict(self) -> Dict[str, Any]:
        # 将 Paragraph 对象转换为字典
        return {
            "id": self.id,
            "page": self.page,
            "text": self.text
        }


@dataclass
class Document:
    paragraphs: List[Paragraph]

    def to_dict(self) -> Dict[str, Any]:
        # 将 Document 对象转换为字典，包含段落列表
        return {
            "paragraphs": [p.to_dict() for p in self.paragraphs]
        }


@dataclass
class DocumentGroup:
    documents: Dict[str, Document]

    def to_dict(self) -> Dict[str, Any]:
        # 将 DocumentGroup 对象转换为字典，包含多个文档
        return {doc_id: doc.to_dict() for doc_id, doc in self.documents.items()}


@dataclass
class DocRoot:
    document_groups: Dict[str, DocumentGroup]

    @staticmethod
    def parse_json_to_dataclasses(json_data, include_group_id: bool = True) -> Optional['DocRoot']:
        """
        从JSON对象解析为DocRoot对象
        :param json_data:
        :return:
        """
        try:
            document_groups = {}
            if include_group_id:
                document_groups = DocRoot.build_object(json_data)
            else:
                document_groups = DocRoot.build_object_without_group_id(json_data)
            return DocRoot(document_groups=document_groups)
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def build_object(json_data) -> Dict[str, Any]:
        """
        构建对象（版本2，去掉原数据中没有groupId)
        :param json_data:
        :return:
        """

        document_groups = {}
        for group_id, group_data in json_data.items():
            documents = {}
            for doc_id, doc_data in group_data.items():
                paragraphs = [
                    Paragraph(
                        id=paragraph.get("id", ""),
                        page=paragraph.get("page", ""),
                        text=paragraph.get("text", "")
                    )
                    for paragraph in doc_data.get("paragraphs", [])
                ]
                documents[doc_id] = Document(paragraphs=paragraphs)
            document_groups[group_id] = DocumentGroup(documents=documents)
        return document_groups

    @staticmethod
    def build_object_without_group_id(json_data) -> Dict[str, Any]:
        """
        构建对象（版本2，去掉原数据中没有groupId)
        :param json_data:
        :return:
        """

        # 为了兼容原来的和新版的，这里模拟一层groupId
        document_groups = {}
        documents = {}
        for doc_id, doc_data in json_data.items():
            paragraphs = [
                Paragraph(
                    id=paragraph.get("id", ""),
                    page=paragraph.get("page", ""),
                    text=paragraph.get("text", "")
                )
                for paragraph in doc_data.get("paragraphs", [])
            ]
            documents[doc_id] = Document(paragraphs=paragraphs)
        document_groups[str(uuid.uuid4())] = DocumentGroup(documents=documents)
        return document_groups

    def to_json(self) -> str:
        # 将 DocRoot 对象转换为 JSON 字符串
        return json.dumps(
            {group_id: group.to_dict() for group_id, group in self.document_groups.items()},
            ensure_ascii=False,
            indent=4
        )

    @classmethod
    def serialize(cls, obj, include_group_id: bool = True) -> Dict[str, Any]:
        if isinstance(obj, cls):
            if include_group_id:
                return {group_id: group.to_dict() for group_id, group in obj.document_groups.items()}
            else:
                first_group_id = next(iter(obj.document_groups))
                return {doc_id: doc.to_dict() for doc_id, doc in
                        obj.document_groups[first_group_id].documents.items()}
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
