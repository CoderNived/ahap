import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';
import InputBar from '../components/InputBar';
import './ChatPage.css';

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeChatId, setActiveChatId] = useState(null);

  const handleSend = async (text) => {
    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: text,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Simulate AI response for now
    setTimeout(() => {
      const aiMessage = {
        id: Date.now() + 1,
        role: 'ai',
        content: 'I have received your message. AI integration coming soon.',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMessage]);
      setIsLoading(false);
    }, 1500);
  };

  const handleNewChat = () => {
    setMessages([]);
    setActiveChatId(null);
  };

  return (
    <div className="chat-page">
      <Sidebar
        onNewChat={handleNewChat}
        activeChatId={activeChatId}
        onSelectChat={setActiveChatId}
      />
      <div className="chat-page__main">
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
        />
        <InputBar
          onSend={handleSend}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}

export default ChatPage;