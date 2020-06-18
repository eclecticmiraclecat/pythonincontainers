# Base image
FROM python

# create the directory if doesn't exist and cd into it
WORKDIR /app

# copy hello.py and start-app.sh into app
COPY hello.py .
COPY start-app.sh .

# install flask
RUN pip install Flask

# startup command
CMD ["/bin/bash", "start-app.sh"]
