import React, { useState } from 'react';
import ChatBox from '../component/ChatBox';
import ThemeToggle from '../component/ThemeToggle';
import { Home } from 'lucide-react';

export default function AssistantPage({ initialQuery, setInitialQuery }) {
  const [chatKey, setChatKey] = useState(0);

  const handleGoHome = () => {
    if (setInitialQuery) setInitialQuery('');
    setChatKey(prev => prev + 1);
  };

  return (
    <div className="h-full relative flex flex-col bg-background overflow-hidden">
      
      {/* Background Decorators */}
      <div className="absolute top-0 left-[-10%] w-[50%] h-[50%] bg-primary/20 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-0 right-[-10%] w-[40%] h-[40%] bg-blue-500/10 rounded-full blur-[100px] pointer-events-none"></div>

      {/* Top Navigation / Branding */}
      <nav className="w-full p-4 sm:p-6 flex justify-between items-center z-50 shrink-0 border-b border-border">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center overflow-hidden shadow-sm border border-border/50">
             <img src="/lords-path-logo.png" alt="Logo" className="w-8 h-8 object-contain" />
          </div>
          <div>
            <h1 className="font-bold text-lg text-text tracking-tight flex items-center gap-2">
              Lord's Pathology
            </h1>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <button 
            onClick={handleGoHome}
            className="p-2 rounded-full glass hover:bg-surface transition-all text-text-muted hover:text-primary duration-300 shadow-sm"
            aria-label="Home"
            title="Go to Home"
          >
            <Home size={20} />
          </button>
          <ThemeToggle />
        </div>
      </nav>

      {/* Main Chat Interface */}
      <main className="w-full flex-1 flex flex-col items-center justify-center z-10 p-2 sm:p-4 min-h-0">
        <ChatBox key={chatKey} initialQuery={initialQuery} setInitialQuery={setInitialQuery} />
      </main>
      
    </div>
  );
}
