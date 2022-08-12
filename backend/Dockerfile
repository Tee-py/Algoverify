FROM python:3.9.13-slim
RUN apt-get update && apt-get -y install sudo
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
USER docker
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./start.sh .
COPY . .
RUN sed -i 's/\r$//g' ./start.sh
RUN chmod +x ./start.sh
RUN pip install "pymongo[srv]"
RUN pip install "uvicorn[standard]"
CMD [ "./start.sh" ]