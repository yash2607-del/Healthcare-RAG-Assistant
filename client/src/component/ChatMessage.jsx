import React from 'react';
import { User, Stethoscope } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export default function ChatMessage({ message, onAction }) {
  const [selectedLab, setSelectedLab] = React.useState('');
  
  const isUser = message.sender === 'user';
  const formatTime = (date) => {
    if (!date) return '';
    return new Intl.DateTimeFormat('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    }).format(new Date(date));
  };

  let displayText = message.text || '';
  const requiresSelection = displayText.includes('[LAB_SELECTION]');
  let centerOptions = [];
  
  if (requiresSelection) {
    displayText = displayText.replace('[LAB_SELECTION]', '').trim();
    // Extract all Center Names from the text using a global regex
    const nameRegex = /Center Name:\s*(.*)/gi;
    let match;
    while ((match = nameRegex.exec(displayText)) !== null) {
      if (match[1]) {
        centerOptions.push(match[1].trim());
      }
    }
    // Remove duplicates if any
    centerOptions = [...new Set(centerOptions)];
  }
  
  const handleSubmitSelection = () => {
    if (selectedLab && onAction) {
      const queryToSend = `Please provide the contact number, working hours, and service available for: ${selectedLab}`;
      onAction(queryToSend);
    }
  };

  return (
    <div className={cn(
      "flex w-full gap-3 px-2 py-1 animate-slide-up items-center",
      isUser ? "flex-row-reverse" : "flex-row"
    )}>
      {/* Avatar */}
      <div className={cn(
        "shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-sm overflow-hidden",
        isUser ? "bg-primary" : "bg-white border border-border/50"
      )}>
        {isUser ? <User size={20} className="text-white" /> : <img src="/lords-path-logo.png" alt="Logo" className="w-8 h-8 object-contain" />}
      </div>

      {/* Bubble */}
      <div className={cn(
        "flex flex-col max-w-[80%]",
        isUser ? "items-end" : "items-start"
      )}>
        <span className="text-[11px] font-semibold text-text-muted px-1 mb-0.5">
          {isUser ? `You • ${formatTime(message.timestamp)}` : formatTime(message.timestamp)}
        </span>
        <div className={cn(
          "px-5 py-2.5 rounded-2xl shadow-sm text-sm whitespace-pre-wrap leading-relaxed",
          isUser 
            ? "bg-primary text-white rounded-tr-none" 
            : "bg-surface text-text border border-border rounded-tl-none"
        )}>
          {displayText}
        </div>
        
        {requiresSelection && !isUser && centerOptions.length > 0 && (
          <div className="mt-3 bg-white p-4 rounded-xl border border-gray-200 shadow-sm w-full max-w-sm">
            <p className="text-sm text-gray-800 mb-4 font-medium">
              Select a center below to see more details like contact numbers and available services:
            </p>
            <div className="mb-4">
              <select
                value={selectedLab}
                onChange={(e) => setSelectedLab(e.target.value)}
                className="w-full p-2.5 text-sm bg-gray-50 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary text-gray-700 outline-none transition-colors"
              >
                <option value="" disabled>Choose a center...</option>
                {centerOptions.map((name, idx) => (
                  <option key={idx} value={name}>{name}</option>
                ))}
              </select>
            </div>
            <button
              onClick={handleSubmitSelection}
              disabled={!selectedLab}
              className="w-full py-2.5 bg-primary text-white font-medium rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
            >
              Submit
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
