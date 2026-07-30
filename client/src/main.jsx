import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

const WIDGET_ID = 'lord-diagnostics-chat-widget';

let container = document.getElementById(WIDGET_ID);
if (!container) {
  container = document.createElement('div');
  container.id = WIDGET_ID;
  document.body.appendChild(container);
}

createRoot(container).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
