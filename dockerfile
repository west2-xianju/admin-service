FROM python:3.11.0
WORKDIR /admin-api
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "admin-service.py"]
EXPOSE 3000