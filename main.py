import shutil
import uuid
from pathlib import Path
from flask import Flask, request, render_template, send_file
import youtube_dl
from youtube_search import YoutubeSearch

app = Flask(__name__)


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/search')
def search():
    query = request.args.get('q')
    results = YoutubeSearch(query, max_results=10).to_dict()
    return render_template('search.html', results=results)


@app.route('/download')
def download():
    url = request.args.get('url')
    file_name = uuid.uuid4().hex
    ydl_opts = {
        'outtmpl': "files/" + file_name + ".%(ext)s",
        'logger': MyLogger(),
        'progress_hooks': [my_hook]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    path = list((Path(__file__).parent/"files").glob(file_name + '.*'))
    resp = send_file(path[0], as_attachment=True)
    shutil.rmtree(path[0].absolute(), ignore_errors=True)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
