FROM python:3

RUN apt-get -y update
RUN apt -y install wget
RUN apt -y install unzip
RUN apt -y install curl

RUN apt-get install -y google-chrome-stable


RUN apt-get install -yqq unzip curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/bin

RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip
RUN unzip chromedriver-linux64.zip -d /usr/bin

# 크로미움 추가
RUN apt-get install -y chromium 

# RUN mkdir chrome
# RUN unzip /tmp/chromedriver.zip chromedriver -d .
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["sleep", "50000000"]
# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]