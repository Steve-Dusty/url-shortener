from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import secrets

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(3), unique=True)

    def __init__(self, long, short):
        self.long = long
        self.short = short


# create tables only once
@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long = request.form['long']
        short = secrets.token_urlsafe(3)
        url = Url(long, short=short)
        db.session.add(url)
        db.session.commit()
        flash(
            f'Your shortened URL has been successfully created: {request.base_url}{short}')
        return render_template('index.html')

    else:  # GET
        return render_template('index.html')


@app.route('/<short>')
def short(short):
    url = Url.query.filter_by(short=short).first_or_404()
    return redirect(url.long)

# clear cache


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
