function Home() {
  return (
    <div>
      <div className="card">
        <h1 className="card-header">Welcome to FastAPI + React Mastery</h1>
        <p>
          This is a comprehensive learning project that demonstrates how to build
          a full-stack application using FastAPI (backend) and React with Vite (frontend).
        </p>
      </div>

      <div className="grid">
        <div className="card">
          <h3 className="card-header">FastAPI Backend</h3>
          <ul style={{ paddingLeft: '1.5rem' }}>
            <li>RESTful API design</li>
            <li>Data validation with Pydantic</li>
            <li>Database integration</li>
            <li>Authentication & security</li>
            <li>WebSockets & real-time features</li>
          </ul>
        </div>

        <div className="card">
          <h3 className="card-header">React Frontend</h3>
          <ul style={{ paddingLeft: '1.5rem' }}>
            <li>Modern React with Hooks</li>
            <li>Vite for fast development</li>
            <li>Axios for API calls</li>
            <li>React Router for navigation</li>
            <li>Responsive design</li>
          </ul>
        </div>

        <div className="card">
          <h3 className="card-header">Getting Started</h3>
          <ol style={{ paddingLeft: '1.5rem' }}>
            <li>Navigate through the menu</li>
            <li>Try creating items and users</li>
            <li>Test authentication flow</li>
            <li>Explore the API documentation at <code>/docs</code></li>
          </ol>
        </div>
      </div>
    </div>
  )
}

export default Home