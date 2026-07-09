import React from 'react';
import { Loader2 } from 'lucide-react';

export default function Loader() {
  return (
    <div className="flex items-center gap-3 p-4 bg-surface rounded-2xl rounded-tl-none border border-border w-fit shadow-sm animate-fade-in">
      <div className="relative flex h-5 w-5">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
        <span className="relative inline-flex rounded-full h-5 w-5 bg-primary/20 items-center justify-center">
          <Loader2 size={12} className="animate-spin text-primary" />
        </span>
      </div>
      <span className="text-text-muted text-sm font-medium animate-pulse-slow">
        Analyzing database...
      </span>
    </div>
  );
}
