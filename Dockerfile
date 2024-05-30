FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

# Gunicornの設定ファイルを指定
CMD ["gunicorn", "config.wsgi:application", "--config", "gunicorn.conf.py"]

EXPOSE 8000