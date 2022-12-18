# Do not use Alpine Linux if you use pandas
# FROM python:3.10-alpine3.16
# bullseye https://wiki.debian.org/DebianReleases
FROM python:3.10-bullseye

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /

# {module_import}:{app_variable}
# equivalent to 'from app import app'
CMD ["gunicorn", "-b", ":8080", "app:app"]