import React, { useState } from 'react';
import { Sparkles, Microscope, MapPin, ChevronLeft } from 'lucide-react';

export default function SuggestedQuestions({ onSelect }) {
  const [view, setView] = useState('main'); // 'main' or 'states'

  const mainCards = [
    {
      title: "Tests & Packages",
      question: "Explore our tests and packages",
      action: () => onSelect("Explore our tests and packages"),
      icon: <Microscope size={20} className="text-blue-500" />
    },
    {
      title: "Nearby Center",
      question: "Find a Nearby Center",
      action: () => setView('states'),
      icon: <MapPin size={20} className="text-green-500" />
    }
  ];

  const states = [
    "Andhra Pradesh",
    "Goa",
    "Gujarat",
    "Karnataka",
    "Maharashtra"
  ];

  return (
    <div className="flex flex-col gap-2 mt-1 w-full">
      <div className="flex items-center gap-1 text-sm font-medium px-2 justify-center mb-1">
        <span>How can I help you today?</span>
      </div>
      
      {view === 'main' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 w-full">
          {mainCards.map((card, idx) => (
            <button
              key={idx}
              onClick={card.action}
              className="flex flex-col items-center justify-center text-center p-2 rounded-xl border border-border/60 bg-surface/40 hover:bg-surface hover:border-primary/50 hover:shadow-lg transition-all duration-300 group"
            >
              <div className="flex flex-col items-center gap-1 mb-1">
                <div className="p-2 rounded-lg bg-background border border-border/50 group-hover:scale-110 transition-transform duration-300 shadow-sm">
                  {card.icon}
                </div>
                <span className="font-semibold text-text text-sm">{card.title}</span>
              </div>
              <p className="text-xs text-text-muted group-hover:text-text transition-colors duration-300 px-2">
                "{card.question}"
              </p>
            </button>
          ))}
        </div>
      ) : (
        <div className="flex flex-col w-full bg-surface border border-border rounded-xl overflow-hidden shadow-sm animate-slide-up">
          <div className="p-3 bg-background border-b border-border flex items-center gap-2">
            <button onClick={() => setView('main')} className="p-1 hover:bg-surface rounded-md transition-colors">
              <ChevronLeft size={18} className="text-text-muted" />
            </button>
            <span className="text-sm font-semibold text-text">Select your State</span>
          </div>
          <div className="flex flex-col max-h-48 overflow-y-auto p-1">
            {states.map(state => (
              <button
                key={state}
                onClick={() => onSelect(`Show me nearby centers in ${state}`)}
                className="text-left p-3 text-sm text-text hover:bg-primary/10 hover:text-primary rounded-lg transition-colors"
              >
                {state}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
