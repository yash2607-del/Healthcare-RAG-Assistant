import React from 'react';
import AssistantPage from './pages/AssistantPage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <>
      <AssistantPage />
      <ToastContainer 
        position="top-right" 
        theme="colored" 
        autoClose={3000} 
        hideProgressBar={false}
      />
    </>
  )
}

export default App;
