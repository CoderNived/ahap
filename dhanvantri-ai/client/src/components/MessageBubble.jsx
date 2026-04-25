import './MessageBubble.css';

function MessageBubble({ message }) {
  const { role, content, timestamp } = message;
  const isUser = role === 'user';

  return (
    <div className={`bubble ${isUser ? 'bubble--user' : 'bubble--ai'}`}>

      {/* Avatar */}
      <div className="bubble__avatar">
        {isUser ? '👤' : '🏥'}
      </div>

      {/* Content */}
      <div className="bubble__body">
        <div className="bubble__content">
          {content}
        </div>

        {/* Disclaimer for AI messages */}
        {!isUser && (
          <p className="bubble__disclaimer">
            ⚠️ This is not a medical diagnosis. Please consult a healthcare professional.
          </p>
        )}

        {/* Timestamp */}
        <span className="bubble__time">
          {new Date(timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
          })}
        </span>
      </div>

    </div>
  );
}

export default MessageBubble;