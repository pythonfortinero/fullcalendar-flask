from flask import Flask, render_template, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)


class Calendar(db.Model):

    __tablename__ = "calendar"
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)

    def __init__(self, date, title):
        self.date = date
        self.title = title

    def __repr__(self):
        return '<date %r>' % self.date

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form_calendar', methods=['GET', 'POST'])
def formCalendar():
    if request.method == 'POST':
        cl = Calendar(request.form['date'], request.form['title'])
        db.session.add(cl)
        db.session.commit()
    return render_template('form_calendar.html')

@app.route('/data')
def data():
    callist = list()
    cl = Calendar.query.all()
    print cl
    for row in cl:
        callist.append({'start': row.date, 'title': row.title})
    #print(cl)
    return Response(json.dumps(callist),  mimetype='application/json')

    #return "hola"

if __name__ == '__main__':
    app.run(debug=True)
