import React, { useState, useEffect } from 'react';
import './TreningLista.css';

const TreningList = () => {

    const [treninzi, setTreninzi] = useState([]);
    const [otvoreniDetalji, setOtvoreniDetalji] = useState({});

    useEffect(() => {
        fetch('http://localhost:5000/')
            .then((response) => response.json())
            .then((data) => setTreninzi(data))
            .catch((error) => console.error('Greška:', error));
    }, []);

    const prikaziDetalje = (id) => {
        if (otvoreniDetalji[id]) {
            const novi = { ...otvoreniDetalji };
            delete novi[id];
            setOtvoreniDetalji(novi);
            return;
        }

        fetch(`http://localhost:5000/api/treninzi/${id}`)
            .then((response) => response.json())
            .then((data) => {
                setOtvoreniDetalji((prethodno) => ({ ...prethodno, [id]: data }));
            })
            .catch((error) => console.error('Greška:', error));
    };

    const obrisiTrening = (id) => {
        const potvrda = window.confirm('Da li si siguran/na da želiš da obrišeš ovaj trening?');
        if (!potvrda) return;

        fetch(`http://localhost:5000/api/treninzi/${id}`, {
            method: 'DELETE',
        })
            .then((response) => response.json())
            .then(() => {
                setTreninzi((prethodniTreninzi) =>
                    prethodniTreninzi.filter((t) => t.id !== id)
                );

                if (otvoreniDetalji[id]) {
                    const novi = { ...otvoreniDetalji };
                    delete novi[id];
                    setOtvoreniDetalji(novi);
                }
            })
            .catch((error) => console.error('Greška pri brisanju:', error));
    };

    return (
        <div className="trening-container">
            <h2>Moji Treninzi</h2>
            <div className="trening-grid">
                {treninzi.map((trening) => (
                    <React.Fragment key={trening.id}>
                        <div className="trening-card">
                            <div className="trening-info">
                                <h3>{trening.naziv}</h3>
                                <p>Datum: {new Date(trening.datum).toLocaleDateString()}</p>
                            </div>
                            <div className="trening-dugmici">
                                <button onClick={() => prikaziDetalje(trening.id)}>
                                    {otvoreniDetalji[trening.id] ? 'Zatvori' : 'Detalji'}
                                </button>
                                <button
                                    className="dugme-obrisi"
                                    onClick={() => obrisiTrening(trening.id)}
                                >
                                    Obriši
                                </button>
                            </div>
                        </div>

                        {otvoreniDetalji[trening.id] && (
                            <div className="trening-detalji">
                                {otvoreniDetalji[trening.id].vezbe.length === 0 ? (
                                    <p>Nema unetih vežbi za ovaj trening.</p>
                                ) : (
                                    <ul>
                                        {otvoreniDetalji[trening.id].vezbe.map((vezba, index) => (
                                            <li key={index}>
                                                <strong>{vezba.ime}</strong>
                                                {vezba.detalji && ` — ${vezba.detalji}`}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </div>
                        )}
                    </React.Fragment>
                ))}
            </div>
        </div>
    );
};

export default TreningList;