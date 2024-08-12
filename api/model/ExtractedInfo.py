import json


class ExtractedInfo:

    def __int__(self):
        pass

    def serialize_to_json(self, file_path):
        # 使用 __dict__ 获取实例的所有属性
        data_dict = self.__dict__
        # 将字典序列化为 JSON 格式并写入文件
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
