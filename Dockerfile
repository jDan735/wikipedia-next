FROM python:3.9
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
cmd [ "DJANGO_DEBUG=1" ]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]
