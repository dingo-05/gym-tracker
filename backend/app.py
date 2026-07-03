from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy


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
    def to_dict(self):
        return {'id': self.id, 'ime': self.ime}
class Misici(db.Model):
    __tablename__ = 'misici'
    id = db.Column(db.Integer, primary_key=True)
    naziv=db.Column(db.String, nullable=False)
    def to_dict(self):
        return {'id': self.id, 'naziv': self.naziv}

class TreningSet(db.Model):
    __tablename__ = 'trening_set'
    redni_br = db.Column(db.Integer, primary_key=True)
    trening_id=db.Column(db.Integer, db.ForeignKey('trening.id'), primary_key=True)
    vezba_id=db.Column(db.Integer, db.ForeignKey('vezbe.id'), primary_key=True)
    kilaza=db.Column(db.Float)
    broj_ponavljanja=db.Column(db.Integer)

class MisiciVezbe(db.Model):
    __tablename__ = 'misici_vezbe'
    misici_id=db.Column(db.Integer, db.ForeignKey('misici.id'), primary_key=True)
    vezbe_id=db.Column(db.Integer, db.ForeignKey('vezbe.id'), primary_key=True)

# endregion


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api/treninzi')
def trening():
    treninzi=Trening.query.all()
    return jsonify([trening.to_dict() for trening in treninzi])
@app.route('/api/vezbe', methods=['POST', 'GET'])
def vezbe():
    if request.method == 'GET':
        vezbe=Vezbe.query.all()
        return jsonify([vezba.to_dict()for vezba in vezbe])
    else:
        request_data = request.get_json()
        naziv=request_data['naziv']
        if naziv.strip()=='' or len(naziv.strip())>67:
            return Response("{'Los naziv':'Naziv mora da bude ne prazan i da ima manje od 67 karaktera'}",status=400)
        else:
            maxid=Vezbe.query.order_by(Vezbe.id.desc()).first()
            if maxid is None:
                maxid=0
            else:
                maxid=maxid.id
            nova_vezba=Vezbe(id=maxid+1, ime=naziv)
            db.session.add(nova_vezba)
            db.session.commit()
            return Response("{'OK':'Uspesno dodata nova vezba'}",status=200)








@app.route('/api/misici')
def misici():
    misici=Misici.query.all()
    return jsonify([misic.to_dict() for misic in misici])


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

        from seed import pokreni_automatski_seed
        pokreni_automatski_seed(db, Misici, Vezbe, MisiciVezbe)

    app.run(host='0.0.0.0', port=5000, debug=True)