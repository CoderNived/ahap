import Sidebar from '../components/Sidebar'
import ChatWindow from '../components/ChatWindow'
import './ChatPage.css'

function ChatPage() {
  return (
    <div className="chat-layout">
      <Sidebar />
      <ChatWindow />
    </div>
  )
}

export default ChatPage