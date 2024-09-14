import jieba
import re


class TextUtils:
    """
    文本处理类
    """

    TECH_STANDARD_KEYWORDS = r'规范|标准|条文|法|条例|要求|指南|办法|设计|技术|系统'
    TECH_STANDARD_BUSINESS_KEYWORDS = '城市|电气|建筑|环保|消防|道路|给水|排水|焊接|空调|工程|钢|土|照明|工业'
    TECH_STANDARD_CODE_KEYWORDS = r'GB|DB|YY|ISO|JB|SL|JT|JG|SY|AQ|CS|IEEE|AS|BS|IE|T'
    TECH_STANDARD_PATTERN1 = f"^([A-Z0-9/\.\-:]+)\s*[-]?\s*([\u4e00-\u9fa5]{2, 40})$"
    TECH_STANDARD_PATTERN2 = "^《([\u4e00-\u9fa5]+)》\s*([A-Z0-9\-]+)?$"

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
        features = [int(bool(re.search(f'(?=.*[\u4e00-\u9fff]{4, 30})(?=.*[A-Z]{2, 10})', text))),
                    int(bool(re.search(r'([A-Z/]+)\s?(\d+)\s?-\s?(\d+)', text))),
                    int(bool(re.search(TextUtils.TECH_STANDARD_CODE_KEYWORDS, text))),
                    int(bool(re.search(f'({TextUtils.TECH_STANDARD_KEYWORDS})', text))),
                    int(bool(re.search(r'[《》\-/（）)(.]', text))),  # 包含特定字符
                    int(bool(re.match(r'^《（\(', text))),  # 以左括号开头
                    int(bool(re.search(r'[》）)]$', text))),  # 以右括号结尾
                    int(bool(re.search(r'[。，：；]', text))),  # 不包含一些符号
                    int(bool(re.search(r'[。，：；]$', text))),  # 不以符号结尾
                    int(bool(re.search(r'(?=.*[A-Z].*[A-Z])(?=.*\d{4,10}).*', text))),
                    int(bool(re.search(TextUtils.TECH_STANDARD_PATTERN1, text))),
                    int(bool(re.search(TextUtils.TECH_STANDARD_PATTERN2, text))),
                    int(bool(re.search(TextUtils.TECH_STANDARD_BUSINESS_KEYWORDS, text))),
                    int(bool(re.search(r'^《[\u4e00-\u9fff]{4,30}》$', text))),
                    len(text),
                    ]
        return features

    @staticmethod
    def fit_tech_standard_pattern(text) -> bool:
        # pattern1 = f"^([{TextUtils.TECH_STANDARD_CODE_KEYWORDS}]+)\s*[-]?\s*([\u4e00-\u9fa5]{2,20})$"
        # pattern2 = "^《([\u4e00-\u9fa5]+)》\s*([{TextUtils.TECH_STANDARD_CODE_KEYWORDS}]+)?$"
        return bool(re.search(TextUtils.TECH_STANDARD_PATTERN1, text)) or bool(
            re.search(TextUtils.TECH_STANDARD_PATTERN2, text))

    @staticmethod
    def not_fit_tech_standard_pattern(text) -> bool:
        return not (bool(re.search(TextUtils.TECH_STANDARD_KEYWORDS, text)) or bool(
            re.search(TextUtils.TECH_STANDARD_CODE_KEYWORDS, text)))
