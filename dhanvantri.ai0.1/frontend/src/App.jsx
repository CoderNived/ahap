import { ThemeProvider } from './context/ThemeContext'
import ChatPage from './pages/ChatPage'

function App() {
  return (
    <ThemeProvider>
      <ChatPage />
    </ThemeProvider>
  )
}

export default App