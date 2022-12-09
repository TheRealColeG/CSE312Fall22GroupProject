#build image based on python
FROM python:3.8

# set the environment variable (HOME) to the value (/root)
ENV HOME /root
# set the working directory
WORKDIR /root

#copy all files or directories to the image
COPY . .

#install pymongo and flask into our application
RUN pip3 install -r requirements.txt

#default port 
EXPOSE 8080

# The docker-compose-wait tool is a small command line utility to wait 
# for other docker images to be started while using docker-compose. 
# It permits to wait for a fixed amount of seconds and/or to wait 
# until a TCP port is open on a target image.
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait

#chmod means "change mode", +x means "execute", content inside /wait will be executed. 
RUN chmod +x /wait

# command for running the application in container
CMD /wait && python3 -u server.py

