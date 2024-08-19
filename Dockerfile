FROM python:3.12.4

ENV PYTHONNUNBUFFERD=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver" ]