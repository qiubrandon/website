FROM python:3.8
RUN apt-get update

ENV HOME /root
WORKDIR /root

COPY . .
# Download dependancies
#RUN pip3 install os sys socketserver

EXPOSE 8080

CMD python3 -u server.py