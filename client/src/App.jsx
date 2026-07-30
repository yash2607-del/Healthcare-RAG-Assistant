import React, { useState } from 'react';
import AssistantPage from './pages/AssistantPage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { MessageSquare, X } from 'lucide-react';
import { FaFlask, FaMapMarkerAlt, FaHome, FaArrowRight, FaStethoscope } from 'react-icons/fa';

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [initialQuery, setInitialQuery] = useState('');

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      {/* Navbar */}
      <header className="bg-white shadow-sm py-4 px-8 flex justify-between items-center z-10 relative">
        <div className="flex items-center gap-3">
          <img src="/lords-path-logo.png" alt="Lord's Pathology Logo" className="w-12 h-12 object-contain" />
          <h1 className="text-2xl font-extrabold text-black">Lord's Pathology</h1>
        </div>
        <nav className="hidden md:flex gap-8 text-gray-600 font-medium">
          <a href="#" className="hover:text-black transition-colors">Home</a>
          <a href="#" className="hover:text-black transition-colors">Book a Test</a>
          <a href="#" className="hover:text-black transition-colors">Locate Centre</a>
          <a href="#" className="hover:text-black transition-colors">Contact Us</a>
        </nav>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col md:flex-row relative">
        {/* Left Side Content */}
        <div className="flex-1 px-8 md:px-16 py-12 md:py-24 flex flex-col justify-center max-w-4xl">
          <h2 className="text-4xl lg:text-5xl font-extrabold text-black leading-tight mb-6 tracking-tight">
            Accurate Diagnostics, <br className="hidden sm:block" /> Delivered <span>Right to You.</span>
          </h2>
          <p className="text-base md:text-lg text-gray-600 mb-10 leading-relaxed max-w-2xl pr-4">
            Experience world-class care with Lord's Pathology. Book home collections, locate 70+ centres, and check pricing instantly with our 24/7 AI Assistant.
          </p>
          
          <div className="flex flex-wrap gap-6 mb-12">
            <div className="flex items-center gap-3 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
              <div className="bg-blue-50 p-3 rounded-full text-blue-600">
                <FaFlask size={24} />
              </div>
              <span className="font-semibold text-gray-700">100+ Tests</span>
            </div>
            <div className="flex items-center gap-3 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
              <div className="bg-green-50 p-3 rounded-full text-green-600">
                <FaMapMarkerAlt size={24} />
              </div>
              <span className="font-semibold text-gray-700">72 Centres</span>
            </div>
            <div className="flex items-center gap-3 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
              <div className="bg-purple-50 p-3 rounded-full text-purple-600">
                <FaHome size={24} />
              </div>
              <span className="font-semibold text-gray-700">Home Collection</span>
            </div>
          </div>
          
          <button className="bg-primary hover:bg-primary-hover text-white font-bold py-4 px-8 rounded-full shadow-lg transition-transform hover:-translate-y-1 w-fit flex items-center gap-2">
            Book Now
            <FaArrowRight />
          </button>
        </div>

        {/* Right side placeholder / image area */}
        <div className="hidden md:flex flex-1 items-center justify-center p-12 relative overflow-hidden">
           {/* Abstract decorative elements */}
           <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-100 rounded-full blur-3xl opacity-50"></div>
           <div className="absolute top-1/4 right-1/4 w-64 h-64 bg-purple-100 rounded-full blur-3xl opacity-50"></div>
        </div>
      </main>

      {/* Floating Chatbot */}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col items-end">
        {isOpen && (
          <div className="w-100 h-187.5 max-h-[calc(100vh-180px)] max-w-[95vw] mb-4 bg-background border border-border rounded-2xl shadow-2xl overflow-hidden flex flex-col animate-slide-up">
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
