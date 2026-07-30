import React, { useState } from 'react';
import AssistantPage from './pages/AssistantPage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { MessageSquare, X } from 'lucide-react';

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [initialQuery, setInitialQuery] = useState('');

  return (
    <div className="fixed bottom-4 right-4 z-9999 flex flex-col items-end font-sans">
      {isOpen && (
        <div className="w-105 h-205 max-h-[calc(100vh-120px)] max-w-[95vw] mb-4 bg-background border border-border rounded-2xl shadow-2xl overflow-hidden flex flex-col animate-slide-up">
           <AssistantPage initialQuery={initialQuery} setInitialQuery={setInitialQuery} />
        </div>
      )}
      <div className="flex items-center gap-3 relative">
        {!isOpen && (
          <div className="flex items-center animate-bounce mr-2">
            <div className="bg-white text-primary text-sm font-bold px-4 py-2 rounded-2xl shadow-lg border border-border relative">
              Chat with us!
              {/* Right pointing arrow */}
              <div className="absolute top-1/2 -right-2 -translate-y-1/2 w-0 h-0 border-y-8 border-y-transparent border-l-8 border-l-border"></div>
              <div className="absolute top-1/2 -right-1.75 -translate-y-1/2 w-0 h-0 border-y-[7px] border-y-transparent border-l-[7px] border-l-white"></div>
            </div>
          </div>
        )}
        
        <button 
          onClick={() => setIsOpen(!isOpen)}
          className="w-14 h-14 bg-primary hover:bg-primary-hover text-white rounded-full flex items-center justify-center shadow-lg transition-transform hover:scale-105 cursor-pointer relative z-10"
        >
          {isOpen ? (
            <X size={24} />
          ) : (
            <div className="w-full h-full rounded-full bg-white flex items-center justify-center overflow-hidden border-2 border-primary shadow-sm p-1">
              <img src="/lords-path-logo.png" alt="Chat" className="w-10 h-10 object-contain" />
            </div>
          )}
        </button>
      </div>

      <ToastContainer 
        position="top-right" 
        theme="colored" 
        autoClose={3000} 
        hideProgressBar={false}
      />
    </div>
  )
}

export default App;
