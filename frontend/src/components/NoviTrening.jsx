import React, { useState, useEffect } from 'react';
import './NoviTrening.css';

const NoviTrening = ({ onTreningKreiran }) => {

    const [naziv, setNaziv] = useState('');
    const [sveVezbe, setSveVezbe] = useState([]);
    const [izabraneVezbe, setIzabraneVezbe] = useState([]);
    const [trenutnaVezbaId, setTrenutnaVezbaId] = useState('');
    const [trenutniDetalji, setTrenutniDetalji] = useState('');

    useEffect(() => {
        fetch('http://localhost:5000/api/vezbe')
            .then((res) => res.json())
            .then((data) => setSveVezbe(data))
            .catch((err) => console.error('Greška pri učitavanju vežbi:', err));
    }, []);

    const dodajVezbu = () => {
        if (!trenutnaVezbaId) return;

        const vezbaObjekat = sveVezbe.find((v) => v.id === parseInt(trenutnaVezbaId));

        setIzabraneVezbe([
            ...izabraneVezbe,
            {
                vezba_id: parseInt(trenutnaVezbaId),
                ime: vezbaObjekat.ime,
                detalji: trenutniDetalji,
            },
        ]);

        setTrenutnaVezbaId('');
        setTrenutniDetalji('');
    };

    const ukloniVezbu = (index) => {
        setIzabraneVezbe(izabraneVezbe.filter((_, i) => i !== index));
    };

    const sacuvajTrening = () => {
        if (!naziv.trim()) {
            alert('Unesi naziv treninga!');
            return;
        }

        const podaciZaSlanje = {
            naziv: naziv,
            vezbe: izabraneVezbe.map((v) => ({
                vezba_id: v.vezba_id,
                detalji: v.detalji,
            })),
        };

        fetch('http://localhost:5000/api/treninzi', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(podaciZaSlanje),
        })
            .then((res) => res.json())
            .then(() => {
                setNaziv('');
                setIzabraneVezbe([]);
                if (onTreningKreiran) onTreningKreiran();
            })
            .catch((err) => console.error('Greška pri čuvanju treninga:', err));
    };

    return (
        <div className="novi-trening-container">
            <h2>Novi Trening</h2>

            <input
                type="text"
                placeholder="Naziv treninga (npr. Trening grudi)"
                value={naziv}
                onChange={(e) => setNaziv(e.target.value)}
                className="input-naziv"
            />

            <div className="dodavanje-vezbe">
                <select
                    value={trenutnaVezbaId}
                    onChange={(e) => setTrenutnaVezbaId(e.target.value)}
                >
                    <option value="">-- Izaberi vežbu --</option>
                    {sveVezbe.map((vezba) => (
                        <option key={vezba.id} value={vezba.id}>
                            {vezba.ime}
                        </option>
                    ))}
                </select>

                <input
                    type="text"
                    placeholder="Serije/ponavljanja/težina"
                    value={trenutniDetalji}
                    onChange={(e) => setTrenutniDetalji(e.target.value)}
                />

                <button onClick={dodajVezbu}>Dodaj vežbu</button>
            </div>

            {izabraneVezbe.length > 0 && (
                <ul className="lista-izabranih-vezbi">
                    {izabraneVezbe.map((vezba, index) => (
                        <li key={index}>
                            <span className="vezba-ime">{vezba.ime}</span>
                            <span className="vezba-detalji">{vezba.detalji}</span>
                            <button
                                className="dugme-ukloni"
                                onClick={() => ukloniVezbu(index)}
                            >
                                ✕
                            </button>
                        </li>
                    ))}
                </ul>
            )}

            <button className="dugme-sacuvaj" onClick={sacuvajTrening}>
                Sačuvaj trening
            </button>
        </div>
    );
};

export default NoviTrening;