FROM python:3

WORKDIR /sheikhs

COPY . /sheikhs

RUN pip install -r requirements.txt

CMD python -mflask --app basic init-db && \
	python -mflask --app basic run -h 0.0.0.0 -p 3000 --debug
