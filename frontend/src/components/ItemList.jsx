import { useState, useEffect } from 'react'
import api from '../api/axios'

function ItemList({ refresh }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchItems()
  }, [refresh])

  const fetchItems = async () => {
    try {
      setLoading(true)
      // Note: This is a mock endpoint. Adjust based on your backend
      const response = await api.get('/search', {
        params: { skip: 0, limit: 10 }
      })
      
      // Mock data for demonstration
      const mockItems = [
        { id: 1, name: 'Laptop', price: 999.99, description: 'High-performance laptop' },
        { id: 2, name: 'Mouse', price: 29.99, description: 'Wireless mouse' },
        { id: 3, name: 'Keyboard', price: 79.99, description: 'Mechanical keyboard' },
      ]
      setItems(mockItems)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch items')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (itemId) => {
    if (!window.confirm('Are you sure you want to delete this item?')) {
      return
    }

    try {
      await api.delete(`/items/${itemId}`)
      setItems(items.filter(item => item.id !== itemId))
    } catch (err) {
      alert('Failed to delete item')
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  if (error) {
    return <div className="alert alert-error">{error}</div>
  }

  return (
    <div className="card">
      <h2 className="card-header">Items List</h2>
      
      {items.length === 0 ? (
        <p>No items found. Create your first item!</p>
      ) : (
        <div className="grid">
          {items.map(item => (
            <div key={item.id} className="item-card">
              <h3>{item.name}</h3>
              <p>{item.description}</p>
              <p><strong>Price:</strong> ${item.price}</p>
              <div className="item-card-actions">
                <button className="btn btn-secondary">Edit</button>
                <button 
                  className="btn btn-danger"
                  onClick={() => handleDelete(item.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ItemList
