from loguru import logger
import joblib
from training.trainer.TechStandardTraining import TechStandardTraining
import json
from typing import Any


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
        files.append(r"D:\标书\技术标\text\56延安宏庆油气工程有限公司.json")

        for file_path in files:
            json_data = read_json_file(file_path)
            texts = [text for text in extract_texts_from_json(json_data) if text.strip()]
            vectors = vectorizer.transform(texts)
            prediction = model.predict(vectors)

            for index, value in enumerate(prediction):
                print(f"{texts[index]}, predict:[{value}]")
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
