import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import 'flowbite'
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from 'react-toastify';

<ToastContainer position="top-right" autoClose={3000} />

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
