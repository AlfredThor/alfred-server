FROM python:3.12

LABEL maintainer="Alfred"

# RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y \
    vim \
    gcc \
    cmake \
    tzdata \
    supervisor && \
    ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo Asia/Shanghai > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*


ENV PYTHONUNBUFFERED 1

WORKDIR /alfred-server

ADD . /alfred-server

RUN /usr/local/bin/python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN cp /alfred-server/construction/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
RUN cp /alfred-server/construction/gunicorn/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]