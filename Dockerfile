# 使用官方的 Python 镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 到容器中
COPY requirements.txt .

# 设置源
RUN pip config set global.index-url https://mirrors.163.com/pypi/simple/

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制当前目录下的所有文件到工作目录
COPY . .

# 暴露 Flask 运行的端口
EXPOSE 5000

# 使用 Gunicorn 运行 Flask 应用
# -w 4：指定使用4个工作进程。可以根据你的服务器CPU核心数和应用负载调整此参数。
# -b 0.0.0.0:5000：绑定到主机的5000端口，允许外部访问。
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api.app:app"]