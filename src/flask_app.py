import json
import threading
import time

import schedule

from flask import Flask
from main import get_all_posts

app = Flask(__name__)
posts = []


def update():
    global posts
    posts = get_all_posts(channel)


@app.route('/')
def root():
    return "Hello World"


@app.route('/posts.json')
def posts():
    return json.dumps(posts, indent=1, ensure_ascii=False)


@app.route('/update')
def update_route():
    update()
    return "Updated"


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    channel = 'hykilp'
    update()

    # Auto update every hour
    def thread_func():
        while True:
            schedule.run_pending()
            time.sleep(2)

    schedule.every().hour.do(update)
    threading.Thread(target=thread_func).start()

    # Start app
    app.run(port=13845)
