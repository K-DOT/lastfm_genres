from app import app
from flask import render_template, jsonify, json, url_for
from app.forms import MainForm
from lastfm import LastFMError, get_track_genre, get_track_count
import celery

@app.route('/', methods=['GET'])
def index():
    form = MainForm()
    return render_template('index.html', form=form)


@app.route('/start_task', methods=['POST'])
def longtask():
    form = MainForm()
    if form.validate_on_submit:
        task = background_task.delay(form.username.data, form.limit.data, form.period.data)
        return jsonify({}), 202, {'Location': url_for('status',
                                                      id_=task.id)}

@app.route('/status/<id_>')
def status(id_):
    task = background_task.AsyncResult(id_)
    if task.ready():
        try:
            return json.dumps(task.get()) 
        except LastFMError as e:
            return jsonify(error=str(e)) 
    return jsonify(state=task.state)

@celery.task(bind=True)
def background_task(self, username, limit, period):
    count = get_track_count(username, limit, period) 
    return get_track_genre(count)   