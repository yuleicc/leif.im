FROM python:3.6.2

# 设置工作目录
RUN mkdir -p /code
WORKDIR /code
COPY ./conf/pip.conf /root/.pip/pip.conf

# 添加依赖（利用Docker 的缓存）
ADD ./requirements/ /code/
ADD ./requirements/*.txt /code/requirements/

# 安装依赖
RUN pip install --upgrade pip && pip install -r requirements/dev.txt

# 添加应用
ADD . /code/

# 运行服务
# CMD python manage.py runserver -h 0.0.0.0