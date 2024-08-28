from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json
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
    def parse_json_to_dataclasses(json_data) -> Optional['DocRoot']:
        """
        从JSON对象解析为DocRoot对象
        :param json_data:
        :return:
        """
        try:
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
            return DocRoot(document_groups=document_groups)
        except Exception as e:
            logger.error(e)
            return None

    def to_json(self) -> str:
        # 将 DocRoot 对象转换为 JSON 字符串
        return json.dumps(
            {group_id: group.to_dict() for group_id, group in self.document_groups.items()},
            ensure_ascii=False,
            indent=4
        )

    @classmethod
    def serialize(cls, obj):
        if isinstance(obj, cls):
            return {group_id: group.to_dict() for group_id, group in obj.document_groups.items()}
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
