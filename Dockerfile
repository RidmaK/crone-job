# syntax=docker/dockerfile:1

# base python image for custom image
FROM python:3.12.1-bookworm

# create working directory and install pip dependencies
WORKDIR /main
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy python project files from local to /app image working directory
COPY . .

# run the flask server  
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]