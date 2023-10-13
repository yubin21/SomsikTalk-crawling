from flask import Flask
from crawling import bp  # crawling.py에서 blueprint를 가져옵니다.


app = Flask(__name__)
app.register_blueprint(bp)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

