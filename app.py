from flask import Flask, render_template, request, redirect
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Info about tour {self.tour_name}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET','POST'])
def send():
    if request.method == 'POST':
        tour = Tour(tour_name=request.form['name'],
                    description=request.form['description'])
        db.session.add(tour)
        db.session.commit()

        return render_template('send.html', name=tour.name, description=tour.description)

    return render_template('send.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)