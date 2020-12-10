import os
import uuid
from pathlib import Path
from flask import Flask, request, render_template, send_file, after_this_request, redirect, send_from_directory
import youtube_dl
from youtube_search import YoutubeSearch
import urllib.parse
import requests

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


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('public/css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('public/js', path)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/search')
def search():
    query = request.args.get('q')
    results = YoutubeSearch(query).to_dict()
    for x in results:
        x["thumbnails"] = urllib.parse.urlencode({'url': x["thumbnails"][0]})
    return render_template('search.html', results=results)


@app.route('/proxy-download')
def proxy_download():
    url = request.args.get('url')
    file_name = uuid.uuid4().hex
    ydl_opts = {
        'outtmpl': "files/%(title)s" + file_name + ".%(ext)s",
        'logger': MyLogger(),
        'progress_hooks': [my_hook]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    path = list((Path(__file__).parent/"files").glob('*' + file_name + '.*'))

    @after_this_request
    def remove_file(response):
        try:
            os.remove(path[0])
            path.close()
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_file(path[0], as_attachment=True)


@app.route('/download')
def download():
    url = request.args.get('url')
    file_name = uuid.uuid4().hex
    ydl_opts = {
        'outtmpl': "files/%(title)s" + file_name + ".%(ext)s",
        'logger': MyLogger(),
        'progress_hooks': [my_hook]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    path = list((Path(__file__).parent/"files").glob('*' + file_name + '.*'))

    @after_this_request
    def remove_file(response):
        try:
            os.remove(path[0])
            path.close()
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_file(path[0], as_attachment=True)


@app.route('/direct-download')
def direct_download():
    url = request.args.get('url')
    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
    return render_template('download.html', formats=info["formats"])


@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    response = requests.get(url)
    return response.content, response.status_code, response.headers.items()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
