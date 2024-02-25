FROM python:latest
WORKDIR /tca-api
COPY requirements.txt /tca-api
RUN pip3 install --upgrade pip -r requirements.txt
COPY . /tca-api
EXPOSE 8080 27017