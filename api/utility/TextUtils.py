import jieba
import re


class TextUtils:
    """
    文本处理类
    """

    TECH_STANDARD_KEYWORDS = r'规范|标准|条文|法|条例|要求|指南'
    TECH_STANDARD_CODE_KEYWORDS = r'GB|DB|YY|ISO|JB|SL|JT|JG|SY|AQ|CS|IEEE|AS|BS|IE'

    @staticmethod
    def chinese_tokenizer(text):
        """
        使用 jieba 分词
        :param text:
        :return: 对文本分词的结果
        """
        return jieba.lcut(text)

    @staticmethod
    # 自定义特征提取函数
    def extract_tech_standard_features(text) -> [int]:
        features = [int(bool(re.search(r'\d', text))),
                    int(bool(re.search(TextUtils.TECH_STANDARD_CODE_KEYWORDS, text))),
                    int(bool(re.search(TextUtils.TECH_STANDARD_KEYWORDS, text))),
                    int(bool(re.search(r'[《》\-/]', text))),
                    int(bool(re.search(r'[a-zA-Z]]', text))),
                    int(bool(re.match(r'^《', text))),
                    int(bool(re.search(r'\(\d{4}年', text))),
                    int(bool(re.search(r'》$', text))),
                    len(text),
                    ]
        return features

    @staticmethod
    def fit_tech_standard_pattern(text) -> bool:
        pattern1 = f"^([A-Z0-9/\.\-:]+)\s*[-]?\s*([\u4e00-\u9fa5]{2,30})$"
        pattern2 = "^《([\u4e00-\u9fa5]+)》\s*([A-Z0-9\-]+)?$"
        # pattern1 = f"^([{TextUtils.TECH_STANDARD_CODE_KEYWORDS}]+)\s*[-]?\s*([\u4e00-\u9fa5]{2,20})$"
        # pattern2 = "^《([\u4e00-\u9fa5]+)》\s*([{TextUtils.TECH_STANDARD_CODE_KEYWORDS}]+)?$"
        return bool(re.search(pattern1, text)) or bool(re.search(pattern2, text))
