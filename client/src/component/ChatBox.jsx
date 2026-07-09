import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Activity } from 'lucide-react';
import { toast } from 'react-toastify';
import ChatMessage from './ChatMessage';
import Loader from './Loader';
import SuggestedQuestions from './SuggestedQuestions';

export default function ChatBox() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: "Hello! I am the Lord Diagnostics AI Assistant. I can help you with test pricing, sample types, and methodologies. How can I assist you today?",
      source: 'chitchat'
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
    const userMsg = { id: Date.now(), sender: 'user', text: text.trim() };
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
        source: response.data.source
      };
      
      setMessages(prev => [...prev, botMsg]);
    } catch (error) {
      console.error(error);
      toast.error('Failed to connect to the server. Is FastAPI running?');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="my-auto flex flex-col min-h-[150px] max-h-full w-full max-w-4xl mx-auto glass rounded-3xl overflow-hidden shadow-2xl border border-border/50 relative transition-all duration-500 ease-in-out">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-2">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {isLoading && <Loader />}
        
        {/* Show suggested questions only at the beginning */}
        {messages.length === 1 && !isLoading && (
          <SuggestedQuestions onSelect={handleSend} />
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-surface/50 border-t border-border/50 backdrop-blur-md">
        <div className="relative flex items-end gap-2 max-w-3xl mx-auto">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about a blood test, price, or methodology..."
            className="w-full min-h-[56px] max-h-[150px] p-4 pr-14 rounded-2xl glass-input resize-none text-sm leading-relaxed"
            rows={1}
            disabled={isLoading}
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || isLoading}
            className="absolute right-2 bottom-2 p-2.5 rounded-xl bg-primary text-white hover:bg-primary-hover disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md"
          >
            <Send size={18} />
          </button>
        </div>
        <p className="text-center text-[10px] text-text-muted mt-3">
          Before booking any test, doctors' consultation is recommended
        </p>
      </div>
    </div>
  );
}
