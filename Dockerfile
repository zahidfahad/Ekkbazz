FROM python:3.11
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ADD requirements.txt /app/
RUN pip3 install -r /app/requirements.txt
COPY . /app