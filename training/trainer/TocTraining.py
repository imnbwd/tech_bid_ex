from sklearn.metrics import classification_report
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from api.utility import TextUtils
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns


class TocTraining:
    """
    目录训练
    """

    # 模型文件路径
    MODEL_PATH = "./saved_models/toc_model.joblib"

    # 词向量文件路径
    VECTORIZER_PATH = "./saved_models/toc_vectorizer.joblib"

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
        joblib.dump(best_rf, TocTraining.MODEL_PATH)

        # 保存vectorizer
        joblib.dump(vectorizer, TocTraining.VECTORIZER_PATH)

    def train_with_multi_models(self, file_name: str) -> None:
        training_data = self.load_training_data(file_name)

        # 将数据转换为特征和标签
        X = [row["content"] for row in training_data]
        y = [row["label"] for row in training_data]

        # 使用TF-IDF向量化文本特征
        vectorizer = TfidfVectorizer(tokenizer=TextUtils.chinese_tokenizer, max_features=1500)
        X_vectorized = vectorizer.fit_transform([' '.join(map(str, row)) for row in X])

        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

        # 定义多个模型
        models = {
            'Logistic Regression': LogisticRegression(),
            'SVM': SVC(),
            'Random Forest': RandomForestClassifier()
        }

        # 用于存储结果的字典
        results = {}

        for model_name, model in models.items():
            # 训练模型
            model.fit(X_train, y_train)

            # 预测
            y_pred = model.predict(X_test)

            # 计算性能指标
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, output_dict=True)

            # 存储结果
            results[model_name] = {
                'accuracy': accuracy,
                'classification_report': report
            }

        # 输出各模型的结果
        for model_name, result in results.items():
            print(f"Model: {model_name}")
            print(f"Accuracy: {result['accuracy']:.4f}")
            print(f"Classification Report: {result['classification_report']}\n")

        # 将结果转换为DataFrame以便绘图
        result_df = pd.DataFrame({
            'Model': list(results.keys()),
            'Accuracy': [result['accuracy'] for result in results.values()]
        })

        # 绘制条形图比较各个模型的准确率
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Accuracy', y='Model', data=result_df, palette='viridis')
        plt.title('Model Comparison - Accuracy')
        plt.show()
