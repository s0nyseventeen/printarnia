FROM python:3-alpine

WORKDIR /sheikhs

COPY requirements.txt /sheikhs

RUN pip install -r /sheikhs/requirements.txt

COPY . /sheikhs

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "-w", "3", "src.wsgi:app"]
