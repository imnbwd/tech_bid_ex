import json


class PdfData:
    def __init__(self):
        self.data = None
        self.source_path = None
        self.page_count = 0

    def serialize_to_json(self, file_path):
        # 使用 __dict__ 获取实例的所有属性
        data_dict = self.__dict__
        # 将字典序列化为 JSON 格式并写入文件
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data_dict, json_file, ensure_ascii=False, indent=4)

    @staticmethod
    def deserialize_from_json(json_content):
        data_dict = json.loads(json_content)

        # 创建一个新的 PdfData 实例
        pdf_data = PdfData()
        # 动态地将读取到的数据赋值给实例的属性
        for key, value in data_dict.items():
            setattr(pdf_data, key, value)
        return pdf_data

    @staticmethod
    def deserialize_from_file(file_path):
        # 从指定的 JSON 文件中读取数据
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data_dict = json.load(json_file)
        # 创建一个新的 PdfData 实例
        pdf_data = PdfData()
        # 动态地将读取到的数据赋值给实例的属性
        for key, value in data_dict.items():
            setattr(pdf_data, key, value)
        return pdf_data