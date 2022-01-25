FROM python:3.8
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONIOENCODING=UTF-8

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app

EXPOSE 8000
CMD ["python", "-u", "main.py"]
