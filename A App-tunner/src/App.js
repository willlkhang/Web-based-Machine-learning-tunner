import logo from './logo.svg';
import './App.css';

import React, {useEffect, useState} from 'react';
import io from 'socket.io-client';

//import UI component
import DataTable from '.components/DataTable';
import Form from '.components/Form';
import Gear from '.components/Gear';
import Header from '.components/Header';
import Message from '.components/Message';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const socket = io('http://localhost:9000');

function App() {

  const [processData, setProgressData] = useState({
    time: 0,
    total_progress: 0,
  });

  const [epochs, setEpochs] = useState('');
  const [lr, setLr] = useState('');
  const [size, setSize] = useState('');
  const [table, setTable] = useState('');
  const [message, setMessage] = useState('');
  const d = new Date();

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />

        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>

        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>

      </header>
    </div>
  );
}

export default App;
