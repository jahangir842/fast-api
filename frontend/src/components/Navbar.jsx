import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-content">
        <Link to="/" className="navbar-brand">
          FastAPI + React
        </Link>
        <ul className="navbar-links">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/items">Items</Link></li>
          <li><Link to="/users">Users</Link></li>
          <li><Link to="/auth">Auth</Link></li>
        </ul>
      </div>
    </nav>
  )
}

export default Navbar