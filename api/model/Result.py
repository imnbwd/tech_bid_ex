from api.app_const import SUCCESS_CODE


class Result:
    """错误信息"""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.success = code == SUCCESS_CODE
        self.data = None

    def to_dict(self):
        """
        输出字典形式
        :return:
        """
        return {
            'code': self.code,
            'success': self.success,
            'message': self.message,
            'data': self.data
        }

    @staticmethod
    def default_success(message):
        """
        返回一个默认的成功Result对象
        :param message: 消息
        :return:
        """
        return Result(SUCCESS_CODE, message)
