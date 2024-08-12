from paddlenlp import Taskflow


class UieHelper:
    _instance = None

    def __init__(self, schema=None):
        self.__schema = schema
        self.__ie = Taskflow("information_extraction", schema=schema, task_path ="../tm")

    @classmethod
    def get_instance(cls, schema=None):
        """
        实现单例模式，通过这个方法获取实例，以解决每次初始化UIE的性能问题
        :param schema:
        :return:
        """
        if cls._instance is None:
            cls._instance = cls(schema)
        return cls._instance

    def set_schema(self, schema):
        self.__schema = schema
        self.__ie.set_schema(schema)

    def extract(self, text):
        return self.__ie(text)
