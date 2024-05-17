FROM python:3.8
LABEL maintainer="Ion-George Todoran"

COPY . /app
WORKDIR /app/techtrends

# change directory to techtrends; install the requirements; initialize Database
RUN pip install -r requirements.txt
RUN python3 init_db.py

# expose port 3111
EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py"]
