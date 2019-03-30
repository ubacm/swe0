FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /srv/swe0

RUN pip install --no-cache-dir --trusted-host pypi.python.org pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --ignore-pipfile

COPY . /srv/swe0

CMD ["gunicorn", "swe0.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "1"]
