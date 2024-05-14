from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, select_autoescape

app = Flask(__name__)
app.secret_key = 'DJ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/Thirukural_db'
db = SQLAlchemy(app)

class Kural(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_number = db.Column(db.Integer, nullable=False)
    couplet_number = db.Column(db.Integer, nullable=False)
    couplet_text = db.Column(db.String, nullable=False)
    meaning = db.Column(db.String, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    kural_results = Kural.query.filter(Kural.couplet_text.ilike(f'%{keyword}%')).all()
    return render_template('search_results.html', keyword=keyword, kural_results=kural_results)

@app.route('/random')
def random_kural():
    random_kural = Kural.query.order_by(db.func.random()).first()
    return render_template('random_kural.html', random_kural=random_kural)

# Define a custom filter to split the couplet text
def split_couplet(couplet_text):
    words = couplet_text.split()
    first_line = ' '.join(words[:4])
    second_line = ' '.join(words[4:])
    return f'{first_line}<br>{second_line}'

# Register the custom filter
app.jinja_env.filters['split_couplet'] = split_couplet

if __name__ == '__main__':
    app.run(debug=True)

