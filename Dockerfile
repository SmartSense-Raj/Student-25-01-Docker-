FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py .
CMD ["uvicorn", "app:app","--host","0.0.0.0", "--port","5000"]

