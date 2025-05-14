FROM python:3.10

WORKDIR /app

COPY . /app/

# 4. نصب وابستگی‌های پروژه
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p /app/db
RUN chmod 777 /app/db

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 math_project.asgi:application"]

#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]