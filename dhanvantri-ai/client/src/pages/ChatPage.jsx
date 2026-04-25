import { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';
import InputBar from '../components/InputBar';
import { checkHealth, checkMLHealth } from '../services/health.service';
import './ChatPage.css';

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeChatId, setActiveChatId] = useState(null);
  const [systemStatus, setSystemStatus] = useState(null);

  useEffect(() => {
    const checkSystems = async () => {
      try {
        const [apiHealth, mlHealth] = await Promise.all([
          checkHealth(),
          checkMLHealth(),
        ]);
        setSystemStatus({
          api: apiHealth.status,
          ml: mlHealth.ml_service.status,
        });
      } catch (error) {
        setSystemStatus({ api: 'error', ml: 'error' });
      }
    };
    checkSystems();
  }, []);

  const handleSend = async (text) => {
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: text,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

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

        {/* Status Bar */}
        {systemStatus && (
          <div className="chat-page__status">
            <span className={`status-dot ${systemStatus.api === 'ok' ? 'status-dot--online' : 'status-dot--offline'}`} />
            <span>API</span>
            <span className={`status-dot ${systemStatus.ml === 'ok' ? 'status-dot--online' : 'status-dot--offline'}`} />
            <span>ML Service</span>
          </div>
        )}

        <ChatWindow messages={messages} isLoading={isLoading} />
        <InputBar onSend={handleSend} isLoading={isLoading} />
      </div>
    </div>
  );
}

export default ChatPage;