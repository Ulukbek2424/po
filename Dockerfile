FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /backend
RUN apt-get update && apt-get  install -y \
    uwsgi \
    mc \
    supervisor \
    cron
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . ./
COPY supervisord.conf /etc/supervisor/conf.d
CMD ["supervisord"]
EXPOSE 8000
