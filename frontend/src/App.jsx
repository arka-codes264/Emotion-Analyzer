import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Home from './components/Home.jsx'
import Visualizations from './pages/Visualizations.jsx'
import PastData from './pages/PastData.jsx'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/visualizations" element={<Visualizations />} />
            <Route path="/past-data" element={<PastData />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
