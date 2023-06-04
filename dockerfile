FROM python:3.11.0
WORKDIR /admin-api
COPY requirements.txt .
RUN pip install -i http://mirrors.cloud.aliyuncs.com/pypi/simple/ --trusted-host mirrors.cloud.aliyuncs.com -r requirements.txt
COPY . .
CMD ["python", "admin-service.py"]
EXPOSE 3000