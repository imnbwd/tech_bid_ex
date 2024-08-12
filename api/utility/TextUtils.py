import jieba


class TextUtils:
    """
    文本处理类
    """

    @staticmethod
    def chinese_tokenizer(text):
        """
        使用 jieba 分词
        :param text:
        :return: 对文本分词的结果
        """
        return jieba.lcut(text)
