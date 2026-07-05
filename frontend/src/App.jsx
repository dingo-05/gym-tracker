import { useState } from 'react';
import TreningList from './components/TreningLista';
import NoviTrening from './components/NoviTrening';

function App() {

  const [osveziKljuc, setOsveziKljuc] = useState(0);

  const osveziListu = () => {
    setOsveziKljuc((prethodna) => prethodna + 1);
  };

  return (
    <div>
      <h1>Gym Tracker</h1>
      <NoviTrening onTreningKreiran={osveziListu} />
      <TreningList key={osveziKljuc} />
    </div>
  )
}

export default App