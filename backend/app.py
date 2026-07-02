# wsgiref import uklonjen jer koristimo standardni Flask server za razvoj

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app = Flask(__name__)

# region DB parametri
USERNAME = 'postgres'
PASSWORD = 'pass'
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'postgres'
#endregion

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False





db = SQLAlchemy(app)
# region Tabele
class Trening(db.Model):
    __tablename__ = 'trening'
    id = db.Column(db.Integer, primary_key=True)
    naziv=db.Column(db.String)
    datum=db.Column(db.DateTime)
    def to_dict(self):
        return {'id': self.id, 'naziv': self.naziv, 'datum': self.datum}
class Vezbe(db.Model):
    __tablename__ = 'vezbe'
    id = db.Column(db.Integer, primary_key=True)
    ime=db.Column(db.String, nullable=False)
class Misici(db.Model):
    __tablename__ = 'misici'
    id = db.Column(db.Integer, primary_key=True)
    naziv=db.Column(db.String, nullable=False)
class Trening_set(db.Model):
    __tablename__ = 'trening_set'
    redni_br = db.Column(db.Integer, primary_key=True)
    trening_id=db.Column(db.Integer, db.ForeignKey('trening.id'), primary_key=True)
    vezba_id=db.Column(db.Integer, db.ForeignKey('vezbe.id'), primary_key=True)
    kilaza=db.Column(db.Float)
    broj_ponavljanja=db.Column(db.Integer)
class Misici_vezbe(db.Model):
    __tablename__ = 'misici_vezbe'
    misici_id=db.Column(db.Integer, db.ForeignKey('misici.id'), primary_key=True)
    vezbe_id=db.Column(db.Integer, db.ForeignKey('vezbe.id'), primary_key=True)
# endregion


@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/trening')
def trening():
    treninzi=Trening.query.all()
    return jsonify([trening.to_dict() for trening in treninzi])
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)