from app import app
from flask import render_template
from app.forms import MainForm
from multiprocessing.pool import ThreadPool
from lastfm import LastFMError, get_track_genre, get_track_count

@app.route('/', methods=['POST', 'GET'])
def index():
    form = MainForm()
    if form.validate_on_submit():
        error = None
        pool = ThreadPool(processes=1)
        try:
            count = get_track_count(form.username.data, form.limit.data, form.period.data)
        except LastFMError as e:
            error = e
            res = None
        else:
            print(count)
            res = pool.apply_async(get_track_genre, (count,)).get()
        return render_template('index.html', form=form, result=res, error=error)
    return render_template('index.html', form=form)