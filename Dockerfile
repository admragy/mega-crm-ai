# استخدم Python رسمي
FROM python:3.12-slim

# مجلد العمل
WORKDIR /app

# نسخ requirements وتثبيت
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود كله
COPY . .

# تشغيل البوت
CMD ["python", "main.py"]
