FROM python:3.10

# 2. تنظیم دایرکتوری کاری داخل کانتینر
WORKDIR /app

# 3. کپی کردن فایل‌های پروژه داخل کانتینر
COPY . /app/

# 4. نصب وابستگی‌های پروژه
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5. ایجاد دایرکتوری برای دیتابیس SQLite
RUN mkdir -p /app/db
RUN chmod 777 /app/db

# 6. باز کردن پورت پیش‌فرض جنگو
EXPOSE 8000

# 7. اجرای مهاجرت‌های دیتابیس و اجرای سرور جنگو
CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 math_project.asgi:application"]

#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]