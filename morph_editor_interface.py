from flask import Flask, request, after_this_request, render_template, session, jsonify, current_app, make_response, config
import json
import functools
from functools import wraps, update_wrapper
import os
import time
import random
from gram_dict import GrammDict


def jsonp(func):
    """
    Wrap JSONified output for JSONP requests.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function


gd = GrammDict()
app = Flask(__name__)
startTime = time.time()
startLemmataRemaining = len(gd.lemmaList) - gd.cur_lemma
# No sessions! Only one client at a time is allowed.


@app.route('/')
def edit_page():
    global startTime
    startTime = time.time()
    return render_template('index.html',
                           settings=gd.settings,
                           time_elapsed=0,
                           lemmata_remaining=startLemmataRemaining)


@app.route('/cur_word')
def cur_word():
    return jsonify({'settings': gd.settings,
                    'contents': render_template('lemma.html',
                                                lemma=gd.get_cur_word(),
                                                settings=gd.settings,
                                                time_elapsed=time.time() - startTime,
                                                lemmata_processed=max(1, startLemmataRemaining - (len(gd.lemmaList) - gd.cur_lemma)),
                                                lemmata_remaining=len(gd.lemmaList) - gd.cur_lemma)})


@app.route('/next_word')
def next_word():
    gd.update_cur_word(request.args.to_dict())
    imgUrl = False
    if random.random() <= 0.03:
        imgUrl = random.randint(1, 1000)
    return jsonify({'settings': gd.settings,
                    'contents': render_template('lemma.html',
                                                img_url=imgUrl,
                                                lemma=gd.get_next_word(),
                                                settings=gd.settings,
                                                time_elapsed=time.time() - startTime,
                                                lemmata_processed=max(1, startLemmataRemaining - (len(gd.lemmaList) - gd.cur_lemma)),
                                                lemmata_remaining=len(gd.lemmaList) - gd.cur_lemma)})


@app.route('/prev_word')
def prev_word():
    gd.update_cur_word(request.args.to_dict())
    return jsonify({'settings': gd.settings,
                    'contents': render_template('lemma.html',
                                                lemma=gd.get_prev_word(),
                                                settings=gd.settings,
                                                time_elapsed=time.time() - startTime + 1,
                                                lemmata_processed=max(1, startLemmataRemaining - (len(gd.lemmaList) - gd.cur_lemma)),
                                                lemmata_remaining=len(gd.lemmaList) - gd.cur_lemma)})


@app.route('/save_dict')
def save_dict():
    gd.update_cur_word(request.args.to_dict())
    gd.save_lemmata()
    gd.save_settings()
    return jsonify({'status': 'saved'})


if __name__ == "__main__":
    app.run(port=5500, host='0.0.0.0', debug=True)
