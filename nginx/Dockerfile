FROM nginx:latest

COPY ./static /static

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/dev.conf /etc/nginx/conf.d/