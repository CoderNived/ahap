import { useState } from 'react';
import './InputBar.css';

function InputBar({ onSend, isLoading }) {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    onSend(input.trim());
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="input-bar">

      {/* Text Input */}
      <textarea
        className="input-bar__textarea"
        placeholder="Describe your symptoms or ask a health question..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={isLoading}
        rows={1}
      />

      {/* Send Button */}
      <button
        className="input-bar__send"
        onClick={handleSend}
        disabled={!input.trim() || isLoading}
      >
        {isLoading ? '⏳' : '➤'}
      </button>

    </div>
  );
}

export default InputBar;