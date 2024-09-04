/* author: Jakub Rozkosz */

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
// import App from './App';
import Router from "./Router";
// import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router />
  </React.StrictMode>
);