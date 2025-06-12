# از یک نسخه سبک پایتون استفاده می‌کنیم
FROM python:3.10-slim

# محل کار داخل کانتینر
WORKDIR /app

# کپی کردن همه فایل‌ها داخل کانتینر
COPY . /app

# نصب وابستگی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# اجرای فایل اصلی ربات
CMD ["python", "main.py"]
