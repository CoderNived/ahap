import './Sidebar.css';

const mockChats = [
  { id: 1, title: 'Headache symptoms analysis' },
  { id: 2, title: 'Blood pressure trends' },
  { id: 3, title: 'Sleep pattern review' },
];

function Sidebar({ onNewChat, activeChatId, onSelectChat }) {
  return (
    <aside className="sidebar">

      {/* Branding */}
      <div className="sidebar__brand">
        <span className="sidebar__logo">🏥</span>
        <h2 className="sidebar__title">Dhanvantri.ai</h2>
      </div>

      {/* New Chat Button */}
      <button
        className="sidebar__new-chat"
        onClick={onNewChat}
      >
        + New Chat
      </button>

      {/* Chat History */}
      <nav className="sidebar__nav">
        <p className="sidebar__nav-label">Recent Chats</p>
        <ul className="sidebar__chat-list">
          {mockChats.map((chat) => (
            <li
              key={chat.id}
              className={`sidebar__chat-item ${activeChatId === chat.id ? 'sidebar__chat-item--active' : ''}`}
              onClick={() => onSelectChat(chat.id)}
            >
              💬 {chat.title}
            </li>
          ))}
        </ul>
      </nav>

      {/* Footer */}
      <div className="sidebar__footer">
        <p className="sidebar__disclaimer">
          ⚠️ Not a medical diagnosis tool
        </p>
      </div>

    </aside>
  );
}

export default Sidebar;