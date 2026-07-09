import React from 'react';
import { Sparkles, Stethoscope, TestTube, Receipt, Microscope } from 'lucide-react';

export default function SuggestedQuestions({ onSelect }) {
  const cards = [
    {
      title: "Routine Checkups",
      question: "What is the net MRP for a Blood Test?",
      icon: <TestTube size={20} className="text-blue-500" />
    },
    {
      title: "Pricing & Cost",
      question: "What is the price of Vitamin D Total?",
      icon: <Receipt size={20} className="text-green-500" />
    },
    {
      title: "Test Methodology",
      question: "Tell me about the PNH Test methodology.",
      icon: <Microscope size={20} className="text-purple-500" />
    },
    {
      title: "Special Profiles",
      question: "What is included in the RMP Total profile?",
      icon: <Stethoscope size={20} className="text-rose-500" />
    }
  ];

  return (
    <div className="flex flex-col gap-4 mt-2 w-full">
      <div className="flex items-center gap-2 text-text-muted text-sm font-medium px-2 justify-center mb-2">
        <Sparkles size={16} className="text-primary animate-pulse" />
        <span>How can I help you today?</span>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full">
        {cards.map((card, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(card.question)}
            className="flex flex-col items-start text-left p-4 rounded-2xl border border-border/60 bg-surface/40 hover:bg-surface hover:border-primary/50 hover:shadow-lg transition-all duration-300 group"
          >
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-background border border-border/50 group-hover:scale-110 transition-transform duration-300">
                {card.icon}
              </div>
              <span className="font-semibold text-text text-sm">{card.title}</span>
            </div>
            <p className="text-xs text-text-muted group-hover:text-text transition-colors duration-300">
              "{card.question}"
            </p>
          </button>
        ))}
      </div>
    </div>
  );
}
