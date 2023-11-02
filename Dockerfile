FROM python:3-alpine

WORKDIR /sheikhs

COPY requirements.txt /sheikhs

RUN pip install -r /sheikhs/requirements.txt

COPY . /sheikhs

ENTRYPOINT python -mflask --app canoe run -h 0.0.0.0 -p 3000 --debug
