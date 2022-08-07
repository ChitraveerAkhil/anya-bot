#Contents of Dockerfile
#Dockerfile to build an image which supports testing our Qxf2 Page Object Model.
FROM ubuntu 
# Essential tools and xvfb
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y \
    software-properties-common \
    unzip \
    curl \
    xvfb 
 
# Chrome browser to run the tests
RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub -o /tmp/google.pub \
    && cat /tmp/google.pub | apt-key add -; rm /tmp/google.pub \
    && echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list \
    && mkdir -p /usr/share/desktop-directories \
    && apt-get -y update && apt-get install -y google-chrome-stable
# Disable the SUID sandbox so that chrome can launch without being in a privileged container
RUN dpkg-divert --add --rename --divert /opt/google/chrome/google-chrome.real /opt/google/chrome/google-chrome \
    && echo "#!/bin/bash\nexec /opt/google/chrome/google-chrome.real --no-sandbox --disable-setuid-sandbox \"\$@\"" > /opt/google/chrome/google-chrome \
    && chmod 755 /opt/google/chrome/google-chrome
 
# Chrome Driver
RUN mkdir -p /opt/selenium \
    && curl http://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip -o /opt/selenium/chromedriver_linux64.zip \
    && cd /opt/selenium; unzip /opt/selenium/chromedriver_linux64.zip; rm -rf chromedriver_linux64.zip; ln -fs /opt/selenium/chromedriver /usr/local/bin/chromedriver;

# display
RUN export DISPLAY=:20
RUN Xvfb :20 -screen 0 1366x768x16 &

# python
RUN export TZ=Asia/Kolkata
RUN apt-get update
RUN apt-get install -y python3 python3-setuptools python3-pip python3-tk

RUN mkdir -p /app/{csv,images,configs}
ADD requirements.txt /app
ADD wordle_solver.py /app
ADD charProp.py /app
ADD fileOperations.py /app
ADD twitterOperations.py /app
COPY run.sh /app
COPY csv /app/csv
COPY configs /app/configs
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ./run.sh