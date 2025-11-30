"use client";

import { useChat } from '@ai-sdk/react';
import { useCalculatorStore } from '@/context/CalculatorContext';
import { Send, Sparkles, Bot, User } from 'lucide-react';
import { useEffect, useRef } from 'react';
import clsx from 'clsx';

export default function ChatPanel() {
  const { state } = useCalculatorStore();
  
  // Pass the calculator state in the body of every request
  const chatHelpers = useChat() as any;
  const { messages = [], input = '', handleInputChange, handleSubmit, isLoading } = chatHelpers;

  // Auto-scroll to bottom
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex flex-col h-full bg-white border-l border-gray-200 shadow-sm relative">
      {/* Header */}
      <div className="p-4 border-b border-gray-100 bg-white flex justify-between items-center sticky top-0 z-10">
        <div>
          <h2 className="font-semibold text-gray-800 flex items-center gap-2">
            <Bot className="w-5 h-5 text-blue-600" />
            Cuby Smart Assistant
          </h2>
          <p className="text-xs text-gray-500">Experto en ahorro de energía</p>
        </div>
        <div className="flex items-center gap-1 bg-blue-50 px-2 py-1 rounded-full border border-blue-100">
          <Sparkles className="w-3 h-3 text-blue-600" />
          <span className="text-[10px] font-medium text-blue-700">Powered by Gemini</span>
        </div>
      </div>
      
      {/* Messages Area */}
      <div className="flex-1 p-4 overflow-y-auto bg-gray-50 space-y-4">
        {messages.length === 0 && (
          <div className="flex justify-start animate-in fade-in slide-in-from-bottom-2 duration-500">
            <div className="bg-white p-4 rounded-2xl rounded-tl-none shadow-sm border border-gray-100 max-w-[85%]">
              <p className="text-sm text-gray-700">
                ¡Hola! Soy CubyBot. 👋 <br/>
                Veo que tienes configurado tu uso a la izquierda. <br/>
                <b>¿Te gustaría saber cómo reducir tu recibo de luz?</b>
              </p>
            </div>
          </div>
        )}

        {messages.map((m: any) => (
          <div
            key={m.id}
            className={clsx(
              "flex w-full",
              m.role === 'user' ? "justify-end" : "justify-start"
            )}
          >
            <div
              className={clsx(
                "p-3 rounded-2xl max-w-[85%] text-sm shadow-sm",
                m.role === 'user'
                  ? "bg-blue-600 text-white rounded-tr-none"
                  : "bg-white text-gray-800 border border-gray-200 rounded-tl-none"
              )}
            >
              {m.role === 'assistant' ? (
                 <div dangerouslySetInnerHTML={{ __html: m.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br/>') }} />
              ) : (
                m.content
              )}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white p-3 rounded-2xl rounded-tl-none shadow-sm border border-gray-100">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t border-gray-100">
        <form onSubmit={(e) => handleSubmit(e, { body: { calculatorState: state } })} className="flex gap-2">
          <input 
            value={input}
            onChange={handleInputChange}
            placeholder="Pregunta sobre tu ahorro..." 
            className="flex-1 p-3 border border-gray-200 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          />
          <button 
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 text-white p-3 rounded-full hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center shadow-md"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}