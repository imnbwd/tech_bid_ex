from trainer import TechStandardTraining, TocTraining
from tester import TechStandardTesting


def train_model_tech_standard() -> None:
    """
    训练技术标准模型
    :return:
    """
    file_path = "./data/tech_standard_data.xlsx"

    tech_standard_training = TechStandardTraining()
    # toc_training.train_with_multi_models(file_path)
    tech_standard_training.train(file_path)


def train_model_toc() -> None:
    """
    目录
    :return:
    """
    file_path = "./data/toc_data.xlsx"

    toc_training = TocTraining()
    # toc_training.train_with_multi_models(file_path)
    toc_training.train(file_path)


def load_and_test_tech_standard_model() -> None:
    """
    加载和测试技术标准模型
    :return:
    """
    tech_standard_testing = TechStandardTesting()
    tech_standard_testing.load_and_test_model()


def main() -> None:
    # 训练技术标准模型
    train_model_tech_standard()
    # 测试技术标准模型
    # load_and_test_tech_standard_model()


if __name__ == "__main__":
    main()
