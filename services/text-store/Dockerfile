# 使用 Python 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制文件
COPY . .

# 安装依赖
RUN pip install -r requirements.txt

# 暴露端口
EXPOSE 4000

# 启动服务
CMD ["python", "app.py"]
