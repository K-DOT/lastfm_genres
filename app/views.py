from app import app
from flask import render_template
from app.forms import MainForm
from multiprocessing.pool import ThreadPool
from lastfm import get_track_genre, get_track_count

@app.route('/', methods=['POST', 'GET'])
def index():
    form = MainForm()
    if form.validate_on_submit():
        pool = ThreadPool(processes=1)
        count = get_track_count(form.username.data,form.limit.data,form.period.data)
        print(count)
        res = pool.apply_async(get_track_genre, (count,)).get()
        return render_template('index.html', form=form, result=res)
    return render_template('index.html', form=form)