FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip    


COPY ./requirements.txt  /app/
RUN apt-get update
RUN apt-get install -y postgresql-client gettext && apt-get clean
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app/
RUN chmod +x /app/entrypoint.sh
# ENTRYPOINT ["/app/entrypoint.sh"]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]