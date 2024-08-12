import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score, recall_score, f1_score
import joblib
from api.utility import TextUtils


class TechStandardTraining:
    # 模型文件路径
    MODEL_PATH = "./saved_models/tech_standard_model.joblib"

    # 词向量文件路径
    VECTORIZER_PATH = "./saved_models/tech_standard_vectorizer.joblib"

    def __init__(self):
        pass

    def load_training_data(self, file_path: str) -> list:
        training_data = []

        sheets = pd.read_excel(file_path, sheet_name=None, header=1)
        data = sheets.items()
        for sheet_name, df in data:
            # adjust_last_column(df)
            for index, row in df.iterrows():
                content = row.iloc[:-1].tolist()  # 前N-1列是数据
                label = row.iloc[-1]  # 最后一列是标签
                training_data.append({"content": content, "label": label})

        return training_data

    # @staticmethod
    # def chinese_tokenizer(text):
    #     """
    #     使用 jieba 分词
    #     :param text:
    #     :return:
    #     """
    #     return jieba.lcut(text)

    def show_data_plot(self, training_data: []):
        """
        显示源数据的比例图
        :param training_data: 读取后的训练数据
        :return:
        """
        # 统计label列中0和1的数量
        # 统计label为0和1的数量
        label_counts = {0: 0, 1: 0}

        for data in training_data:
            label = data['label']
            if label in label_counts:
                label_counts[label] += 1

        # 使用Matplotlib绘制比例图
        labels = list(label_counts.keys())
        counts = list(label_counts.values())

        # 绘制矩形图（柱状图）
        plt.figure(figsize=(8, 6))
        plt.bar(labels, counts, color=['skyblue', 'lightgreen'])

        # 设置标题和标签
        plt.title('Proportion of Labels 0 and 1')
        plt.xlabel('Label')
        plt.ylabel('Count')

        # 显示每个柱子的数量
        for i, count in enumerate(counts):
            plt.text(labels[i], count + 0.05, str(count), ha='center', va='bottom')

        plt.xticks(labels)  # 设置x轴刻度
        plt.show()

    def train(self, file_name: str) -> None:
        training_data = self.load_training_data(file_name)

        # 将数据转换为特征和标签
        X = [row["content"] for row in training_data]
        y = [row["label"] for row in training_data]

        # 使用TF-IDF向量化文本特征
        vectorizer = TfidfVectorizer(tokenizer=TextUtils.chinese_tokenizer, max_features=1500)
        X_vectorized = vectorizer.fit_transform([' '.join(map(str, row)) for row in X])

        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

        # 训练模型
        # model = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_split=5, min_samples_leaf=2,
        #                                random_state=42)
        model = RandomForestClassifier(random_state=42)

        # 定义参数网格
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['auto', 'sqrt', 'log2']
        }

        # 初始化网格搜索
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid,
                                   cv=5, n_jobs=-1, verbose=2)
        grid_search.fit(X_train, y_train)
        # 输出最佳参数
        print(f"Best Parameters: {grid_search.best_params_}")

        # 使用最佳参数在测试集上进行预测
        best_rf = grid_search.best_estimator_
        y_pred = best_rf.predict(X_test)

        # 计算精确度、召回率和F1值
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        print(f"精确度: {precision:.4f}")
        print(f"召回率: {recall:.4f}")
        print(f"F1值: {f1:.4f}")

        # 如果需要更详细的分类报告
        print("\n分类报告:")
        print(classification_report(y_test, y_pred))

        # 保存模型
        joblib.dump(best_rf, TechStandardTraining.MODEL_PATH)

        # 保存vectorizer
        joblib.dump(vectorizer, TechStandardTraining.VECTORIZER_PATH)
