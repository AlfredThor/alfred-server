FROM nginx:latest

LABEL maintainer="Alfred"

RUN apt-get update -y && \
    apt-get install -y vim && \
    mkdir /log && \
    touch /log/success.log && \
    touch /log/error.log && \
    chmod -R 755 /usr/share/nginx/html && \
    chown -R nginx:nginx /usr/share/nginx/html

ADD conf/nginx.conf /etc/nginx/nginx.conf