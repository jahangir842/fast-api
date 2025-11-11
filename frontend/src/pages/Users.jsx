import { useState, useEffect } from 'react'
import UserForm from '../components/UserForm'
import api from '../api/axios'

function Users() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const response = await api.get('/users')
      setUsers(response.data)
    } catch (err) {
      console.error('Failed to fetch users:', err)
      // Mock data for demonstration
      setUsers([
        { id: 1, username: 'john_doe', email: 'john@example.com', full_name: 'John Doe' },
        { id: 2, username: 'jane_smith', email: 'jane@example.com', full_name: 'Jane Smith' },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleUserCreated = (newUser) => {
    setUsers(prev => [...prev, newUser])
  }

  const handleDeleteUser = async (id) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await api.delete(`/users/${id}`)
        setUsers(prev => prev.filter(user => user.id !== id))
      } catch (err) {
        console.error('Failed to delete user:', err)
        alert('Failed to delete user')
      }
    }
  }

  const handleUpdateUser = async (id, updatedData) => {
    try {
      const response = await api.put(`/users/${id}`, updatedData)
      setUsers(prev => prev.map(user => 
        user.id === id ? { ...user, ...response.data } : user
      ))
    } catch (err) {
      console.error('Failed to update user:', err)
      alert('Failed to update user')
    }
  }

  return (
    <div className="container">
      <h1 style={{ marginBottom: '2rem' }}>User Management</h1>
      
      <UserForm onUserCreated={handleUserCreated} />

      <div className="card" style={{ marginTop: '2rem' }}>
        <h2 className="card-header">Users List</h2>
        
        {loading ? (
          <div className="loading"><div className="spinner"></div></div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Full Name</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.username}</td>
                  <td>{user.email}</td>
                  <td>{user.full_name}</td>
                  <td>
                    <button 
                      className="btn btn-sm btn-outline-primary"
                      style={{ marginRight: '0.5rem' }}
                      onClick={() => {
                        const newFullName = prompt('Enter new full name:', user.full_name)
                        if (newFullName && newFullName !== user.full_name) {
                          handleUpdateUser(user.id, { full_name: newFullName })
                        }
                      }}
                    >
                      Edit
                    </button>
                    <button 
                      className="btn btn-sm btn-outline-danger"
                      onClick={() => handleDeleteUser(user.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <style jsx>{`
        .container {
          padding: 2rem;
          max-width: 1200px;
          margin: 0 auto;
        }
        
        .card {
          background: white;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          overflow: hidden;
        }
        
        .card-header {
          background: #f8f9fa;
          padding: 1rem 1.5rem;
          margin: 0;
          border-bottom: 1px solid #dee2e6;
        }
        
        .table {
          width: 100%;
          border-collapse: collapse;
        }
        
        .table th,
        .table td {
          padding: 0.75rem;
          text-align: left;
          border-bottom: 1px solid #dee2e6;
        }
        
        .table th {
          background: #f8f9fa;
          font-weight: 600;
        }
        
        .table tr:hover {
          background-color: #f8f9fa;
        }
        
        .btn {
          padding: 0.375rem 0.75rem;
          border: 1px solid transparent;
          border-radius: 0.25rem;
          cursor: pointer;
          text-decoration: none;
          display: inline-block;
          font-size: 0.875rem;
          line-height: 1.5;
        }
        
        .btn-sm {
          padding: 0.25rem 0.5rem;
          font-size: 0.875rem;
        }
        
        .btn-outline-primary {
          color: #0d6efd;
          border-color: #0d6efd;
        }
        
        .btn-outline-primary:hover {
          background-color: #0d6efd;
          color: white;
        }
        
        .btn-outline-danger {
          color: #dc3545;
          border-color: #dc3545;
        }
        
        .btn-outline-danger:hover {
          background-color: #dc3545;
          color: white;
        }
        
        .loading {
          display: flex;
          justify-content: center;
          align-items: center;
          padding: 2rem;
        }
        
        .spinner {
          width: 2rem;
          height: 2rem;
          border: 2px solid #f3f3f3;
          border-top: 2px solid #0d6efd;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}

export default Users