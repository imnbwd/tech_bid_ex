from loguru import logger
import joblib
from training.trainer.TechStandardTraining import TechStandardTraining
from training.trainer.TocTraining import TocTraining
import json
import scipy.sparse as sp
import time
from api.utility import TextUtils
from sklearn.feature_selection import SelectKBest, f_classif
import numpy as np


def extract_texts_from_json(json_data) -> list[str]:
    texts = []
    for key1, value1 in json_data.items():
        for key2, value2 in value1.items():
            paragraphs = value2.get("paragraphs", [])
            for paragraph in paragraphs:
                text = paragraph.get("text", "").strip()  # 去掉前后空白字符
                if text:
                    texts.append(text)
    return texts


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


class TechStandardTesting:

    def load_and_test_model(self) -> None:
        try:
            model = joblib.load(TechStandardTraining.MODEL_PATH)
            vectorizer = joblib.load(TechStandardTraining.VECTORIZER_PATH)
        except Exception as e:
            logger.exception(e)

        print("加载模型成功")
        files = []
        files.append(r"F:\保利国际广场项目土建及水电安装工程技术标-合稿.json")
        files.append(r"F:\电力领域.json")

        for file_path in files:
            json_data = read_json_file(file_path)
            texts = [text for text in extract_texts_from_json(json_data) if text.strip()]
            vectors = vectorizer.transform(texts)

            custom_features = [TextUtils.extract_tech_standard_features(row[0]) for row in texts]
            vectors = sp.hstack((vectors, custom_features))

            # 使用特征选择
            feature_indices = np.load(TechStandardTraining.FEATURE_INDEX_PATH)
            vectors = vectors.toarray()[:, feature_indices]

            prediction = model.predict(vectors)
            for i, text in enumerate(texts):
                if TextUtils.fit_tech_standard_pattern(text):
                    prediction[i] = 1

            for index, value in enumerate(prediction):
                print(f"{texts[index]}, predict:[{value}]\n")
                # if value == 1:
                #     
                # else:
                #     print(f"{texts[index], {value}")
                # 打印每一行文本，去掉空行
                # for text in texts:
                #     if text.strip():  # 进一步确认不是空白字符串
                #         text_vector = vectorizer.transform([text])
                #         prediction = model.predict(text_vector)
                #
                #         result = '技术标准' if prediction[0] == 1 else '非技术标准'
                #         print(f"{text} predict: {prediction}, {result}")

    def perf_test(self) -> None:
        try:
            model = joblib.load(TechStandardTraining.MODEL_PATH)
            vectorizer = joblib.load(TechStandardTraining.VECTORIZER_PATH)
        except Exception as e:
            logger.exception(e)

        print("加载模型成功")

        start_time = time.time()
        print(start_time)
        # 待预测的文本
        texts = ["信息报告程序",
                 "通过前面章节的介绍，我们已经对 Transformers 库有了基本的了解，并且上手微调了一个句子对分类模型。从本章开始，我们将通过一系列的实例向大家展示如何使用 Transformers 库来完成目前主流的 NLP 任务。",
                 "GB5032454-50259-96《电气装置安装工程施工及验收规范》",
                 "GB507234-2012《医用气体工程技术规范》",
                 "GB9706.1-2007《医用电气设备第十部分:通用安全要求》",
                 "这是医用电气设备说明",
                 "认真落实施工组织设计中安全技术管理的各项措施，严格执行安全技术措施审批制度、施工项目安全交底制度和设施、设备交接验收使用制度。",
                 "安全管理组织保证体系及责任",
                 "督促、组织机械设备使用前的验收，验收合格后，履行签字手续。",
                 "《制冷设备、空气分离设备安装工程施工及验收规范》 GB50274-2010"]

        count = 0
        while count <= 100:
            vectors = vectorizer.transform(texts)
            prediction = model.predict(vectors)
            count += 1

        # while count <= 100:
        #     for text in texts:
        #         vectors = vectorizer.transform([text])
        #         prediction = model.predict(vectors)
        #     count += 1

        end_time = time.time()
        print(end_time)
        execution_time = end_time - start_time
        print(f"循环执行时间: {execution_time} 秒")

    def perf_test2(self) -> None:
        try:
            model = joblib.load(TechStandardTraining.MODEL_PATH)
            vectorizer = joblib.load(TechStandardTraining.VECTORIZER_PATH)
        except Exception as e:
            logger.exception(e)

        print("加载模型成功")

        start_time = time.time()

        files = []
        for i in range(10):
            files.append(r"D:\标书\技术标\text\56延安宏庆油气工程有限公司.json")

        for file_path in files:
            json_data = read_json_file(file_path)
            texts = [text for text in extract_texts_from_json(json_data) if text.strip()]
            vectors = vectorizer.transform(texts)
            prediction = model.predict(vectors)

            # for index, value in enumerate(prediction):
            #     print(f"{texts[index]}, predict:[{value}]")

        end_time = time.time()
        print(end_time)
        execution_time = end_time - start_time
        print(f"循环执行时间: {execution_time} 秒")
