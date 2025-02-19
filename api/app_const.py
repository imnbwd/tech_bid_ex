from enum import Enum
from typing import Optional

SUCCESS_CODE = 10000

STR_ONE = "1"
STR_ZERO = "0"


users = {
    "yqb": {"credential": "7Kj#mRpL9q@X"}
}

APP_SECRET_KEY = "'3a7e9be1f92e27d227de4548214d7c393bc2325b0b1f8e5e4b0c81574c7bc5d6'"


class ServiceType(Enum):
    """
    服务类型枚举
    """

    # 提取服务
    INFO_EXTRACTED = 100

    # 无效内容识别
    INVALID_CONTENT_IDENTIFY = 101

    @staticmethod
    def get_service_by_value(value: int) -> Optional['ServiceType']:
        """
        根据指定的值返回相应的枚举，如找不到返回None
        :param value:
        :return:
        """
        try:
            return ServiceType(value)
        except ValueError:
            return None


class InvalidContentType(Enum):
    """
    无效内容的类型枚举
    """
    # 技术标准
    TECH_STANDARD = "tech_standard"
    # 目录
    TABLE_OF_CONTENT = "table_of_content"

    @staticmethod
    def get_enum_by_value(value: str) -> Optional['InvalidContentType']:
        """
        根据指定的值返回相应的枚举，如找不到返回None
        :param value:
        :return:
        """
        try:
            return InvalidContentType(value)
        except ValueError:
            return None

    @staticmethod
    def get_all_values() -> [str]:
        """
        所有的值
        :return:
        """
        values = [item.value for item in InvalidContentType]
        return values
