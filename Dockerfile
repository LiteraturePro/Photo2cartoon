# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM webforgelabs/dlib:19.9-stretch

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENV GOOGLE_APPLICATION_CREDENTIALS "./token.json"

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg

# Install production dependencies.
RUN pip install --upgrade pip

#RUN pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

#RUN pip install -r requirements.txt 

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Heroku Start command
# CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app
# General Start command
CMD exec gunicorn --bind 0.0.0.0:9000 --workers 1 --threads 8 --timeout 0 app:app
