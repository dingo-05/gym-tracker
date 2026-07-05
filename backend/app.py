import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# region DB parametri
USERNAME = os.environ.get('DB_USERNAME', 'postgres')
PASSWORD = os.environ.get('DB_PASSWORD', 'pass')
HOST = os.environ.get('DB_HOST', 'localhost')
PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'postgres')
# endregion

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# region Tabele

class Trening(db.Model):
    __tablename__ = 'trening'
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String)
    datum = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'naziv': self.naziv, 'datum': self.datum}


class Vezbe(db.Model):
    __tablename__ = 'vezbe'
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'ime': self.ime}


class TreningVezbaDetalji(db.Model):
    __tablename__ = 'trening_vezba_detalji'
    trening_id = db.Column(db.Integer, db.ForeignKey('trening.id', ondelete='CASCADE'), primary_key=True)
    vezba_id = db.Column(db.Integer, db.ForeignKey('vezbe.id', ondelete='CASCADE'), primary_key=True)
    detalji = db.Column(db.Text)

    def to_dict(self):
        return {
            'trening_id': self.trening_id,
            'vezba_id': self.vezba_id,
            'detalji': self.detalji
        }


# endregion



@app.route('/', methods=['GET'])
def trening():
    treninzi = Trening.query.order_by(Trening.datum.desc()).all()
    return jsonify([trening.to_dict() for trening in treninzi]) , 200

@app.route('/api/vezbe', methods=['GET'])
def prikazi_sve_vezbe():
    vezbe = Vezbe.query.order_by(Vezbe.ime).all()
    return jsonify([vezba.to_dict() for vezba in vezbe]), 200

@app.route('/api/treninzi', methods=['POST'])
def kreiraj_trening():
    request_data = request.get_json()

    naziv = request_data.get('naziv', 'Novi Trening')


    novi_trening = Trening(naziv=naziv)
    db.session.add(novi_trening)
    db.session.flush()


    lista_vezbi = request_data.get('vezbe', [])
    for stavka in lista_vezbi:
        v_id = stavka.get('vezba_id')
        detalji_tekst = stavka.get('detalji', '')

        if v_id:
            novi_detalji = TreningVezbaDetalji(
                trening_id=novi_trening.id,
                vezba_id=v_id,
                detalji=detalji_tekst
            )
            db.session.add(novi_detalji)


    db.session.commit()

    return jsonify({
        'status': 'OK',
        'poruka': 'Trening uspešno sačuvan sa automatskim datumom!',
        'trening_id': novi_trening.id
    }), 201

@app.route('/api/treninzi/<int:trening_id>', methods=['GET'])
def prikazi_trening(trening_id):
    trening = Trening.query.get(trening_id)

    if not trening:
        return jsonify({'status': 'Greska', 'poruka': 'Trening nije pronadjen!'}), 404

    stavke = TreningVezbaDetalji.query.filter_by(trening_id=trening_id).all()

    vezbe_lista = []
    for stavka in stavke:
        vezba = Vezbe.query.get(stavka.vezba_id)
        vezbe_lista.append({
            'vezba_id': stavka.vezba_id,
            'ime': vezba.ime if vezba else None,
            'detalji': stavka.detalji
        })

    return jsonify({
        'id': trening.id,
        'naziv': trening.naziv,
        'datum': trening.datum,
        'vezbe': vezbe_lista
    }), 200


@app.route('/api/treninzi/<int:trening_id>', methods=['DELETE'])
def obrisi_trening(trening_id):

    trening = Trening.query.get(trening_id)


    if not trening:
        return jsonify({'status': 'Greska', 'poruka': 'Trening nije pronadjen!'}), 404

    db.session.delete(trening)
    db.session.commit()

    return jsonify({'status': 'OK', 'poruka': f'Trening sa ID {trening_id} je uspesno obrisan!'}), 200



if __name__ == '__main__':
    with app.app_context():

        db.create_all()

        from seed import pokreni_automatski_seed
        pokreni_automatski_seed(db, Vezbe)
    app.run(host='0.0.0.0', port=5000, debug=True)