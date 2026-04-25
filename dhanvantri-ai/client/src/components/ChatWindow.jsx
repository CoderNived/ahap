import { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import './ChatWindow.css';

function ChatWindow({ messages, isLoading }) {
  const bottomRef = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-window">

      {/* Empty State */}
      {messages.length === 0 && !isLoading && (
        <div className="chat-window__empty">
          <span className="chat-window__empty-icon">🏥</span>
          <h2>Welcome to Dhanvantri.ai</h2>
          <p>Describe your symptoms or upload medical data to get started.</p>
          <p className="chat-window__empty-disclaimer">
            ⚠️ This tool provides health insights only — not medical diagnosis or treatment advice.
          </p>
        </div>
      )}

      {/* Messages */}
      <div className="chat-window__messages">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
      </div>

      {/* Loading Indicator */}
      {isLoading && (
        <div className="chat-window__loading">
          <span>🏥</span>
          <span className="chat-window__loading-text">Analyzing...</span>
        </div>
      )}

      {/* Scroll anchor */}
      <div ref={bottomRef} />

    </div>
  );
}

export default ChatWindow;