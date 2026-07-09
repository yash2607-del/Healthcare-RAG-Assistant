import React from 'react';
import ChatBox from '../component/ChatBox';
import ThemeToggle from '../component/ThemeToggle';

export default function AssistantPage() {
  return (
    <div className="h-screen relative flex flex-col bg-background" style={{overflow: 'clip'}}>
      
      {/* Background Decorators */}
      <div className="absolute top-0 left-[-10%] w-[50%] h-[50%] bg-primary/20 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-0 right-[-10%] w-[40%] h-[40%] bg-blue-500/10 rounded-full blur-[100px] pointer-events-none"></div>

      {/* Top Navigation / Branding */}
      <nav className="w-full p-4 sm:p-6 sm:px-12 flex justify-between items-center z-50 flex-shrink-0">
        <div className="flex flex-col">
          <h1 className="text-xl font-bold tracking-tight text-text">
            Lord Diagnostics<span className="text-primary">.ai</span>
          </h1>
          <p className="text-xs text-text-muted font-medium">Smart Health AI</p>
        </div>
        <ThemeToggle />
      </nav>

      {/* Main Chat Interface */}
      <main className="w-full flex-1 flex flex-col items-center justify-center z-10 p-4 sm:p-8 pb-6 min-h-0">
        <ChatBox />
      </main>
      
    </div>
  );
}
