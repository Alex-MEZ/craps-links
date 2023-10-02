FROM python:3.8

ENV DJANGO_SETTINGS_MODULE=craps_links.settings
ENV PYTHONUNBUFFERED 1

RUN mkdir /craps_links
WORKDIR /craps_links

COPY . /craps_links/

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
