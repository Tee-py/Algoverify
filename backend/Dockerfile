FROM python:3.9.13-slim
RUN apt-get update
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install "pymongo[srv]"
COPY ./start.sh .
COPY . .
RUN sed -i 's/\r$//g' ./start.sh
RUN chmod +x ./start.sh
CMD [ "./start.sh" ]