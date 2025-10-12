import { Link, NavLink } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="bg-blue-600 text-white p-4">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <Link to="/" className="text-xl font-semibold tracking-wide">Emotion Tracker</Link>
        <div className="flex gap-6">
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              `hover:opacity-90 transition ${isActive ? 'underline underline-offset-4' : ''}`
            }
          >
            Home
          </NavLink>
          <NavLink
            to="/visualizations"
            className={({ isActive }) =>
              `hover:opacity-90 transition ${isActive ? 'underline underline-offset-4' : ''}`
            }
          >
            Visualizations
          </NavLink>
          <NavLink
            to="/past-data"
            className={({ isActive }) =>
              `hover:opacity-90 transition ${isActive ? 'underline underline-offset-4' : ''}`
            }
          >
            Past Data
          </NavLink>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
