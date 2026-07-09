import React from 'react';
import { User, Stethoscope } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export default function ChatMessage({ message }) {
  const isUser = message.sender === 'user';

  return (
    <div className={cn(
      "flex w-full gap-4 p-4 animate-slide-up",
      isUser ? "flex-row-reverse" : "flex-row"
    )}>
      {/* Avatar */}
      <div className={cn(
        "flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-sm",
        isUser ? "bg-primary text-white" : "bg-surface border border-border text-primary"
      )}>
        {isUser ? <User size={20} /> : <Stethoscope size={20} />}
      </div>

      {/* Bubble */}
      <div className={cn(
        "max-w-[80%] flex flex-col gap-1",
        isUser ? "items-end" : "items-start"
      )}>
        <span className="text-xs font-medium text-text-muted px-1">
          {isUser ? 'You' : 'Lord Diagnostics AI'}
        </span>
        <div className={cn(
          "px-5 py-3 rounded-2xl shadow-sm text-sm whitespace-pre-wrap leading-relaxed",
          isUser 
            ? "bg-primary text-white rounded-tr-none" 
            : "bg-surface text-text border border-border rounded-tl-none"
        )}>
          {message.text}
        </div>
        
       
      </div>
    </div>
  );
}
