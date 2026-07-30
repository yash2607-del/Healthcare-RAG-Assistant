import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Activity } from 'lucide-react';
import { toast } from 'react-toastify';
import ChatMessage from './ChatMessage';
import Loader from './Loader';
import SuggestedQuestions from './SuggestedQuestions';

export default function ChatBox({ initialQuery, setInitialQuery }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: "Welcome to Lord's pathology! Your trusted partner in health with accurate test information, nearby centers, and compassionate care. How can we assist you today?",
      source: 'chitchat',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages, isLoading]);


  const handleSend = async (queryText) => {
    const text = queryText || input;
    if (!text.trim()) return;

    // Add user message
    const userMsg = { id: Date.now(), sender: 'user', text: text.trim(), timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/api/chat', {
        query: text.trim(),
        session_id: 'web_session_1'
      });
      
      const botMsg = { 
        id: Date.now() + 1, 
        sender: 'bot', 
        text: response.data.answer,
        source: response.data.source,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botMsg]);
    } catch (error) {
      console.error(error);
      toast.error('Failed to connect to the server. Is FastAPI running?');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (initialQuery) {
      handleSend(initialQuery);
      if (setInitialQuery) setInitialQuery('');
    }
  }, [initialQuery]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full w-full max-w-4xl mx-auto glass rounded-3xl overflow-hidden shadow-2xl border border-border/50 relative transition-all duration-500 ease-in-out">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-3 pt-4 pb-1 space-y-2 flex flex-col">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} onAction={handleSend} />
        ))}
        {isLoading && <Loader />}
        
        {/* Show suggested questions only at the beginning */}
        {messages.length === 1 && !isLoading && (
          <SuggestedQuestions onSelect={handleSend} />
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-3 pb-4 bg-surface/50 border-t border-border/50 backdrop-blur-md">
        <div className="relative flex items-end gap-2 max-w-3xl mx-auto">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about a blood test, price, or methodology or nearby centers..."
            className="w-full min-h-11 max-h-30 py-2 px-3 pr-12 rounded-xl bg-white border-2 border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/20 resize-none text-sm text-black placeholder:text-gray-700 shadow-sm transition-all"
            rows={2}
            disabled={isLoading}
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || isLoading}
            className="absolute right-1.5 bottom-1.5 p-2 rounded-lg bg-primary text-white hover:bg-primary-hover disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md"
          >
            <Send size={16} />
          </button>
        </div>
        <p className="text-center text-[10px] font-semibold mt-2 mb-0 text-text-muted">
          Before consulting about test, doctor recommendation is needed
        </p>
      </div>
    </div>
  );
}
