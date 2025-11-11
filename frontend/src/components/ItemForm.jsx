import { useState } from 'react'
import api from '../api/axios'

function ItemForm({ onItemCreated }) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    tax: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      const payload = {
        name: formData.name,
        description: formData.description || null,
        price: parseFloat(formData.price),
        tax: formData.tax ? parseFloat(formData.tax) : null
      }

      const response = await api.post('/items', payload)
      setSuccess(true)
      setFormData({ name: '', description: '', price: '', tax: '' })
      
      if (onItemCreated) {
        onItemCreated(response.data)
      }

      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create item')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2 className="card-header">Create New Item</h2>
      
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">Item created successfully!</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name *</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            placeholder="Enter item name"
          />
        </div>

        <div className="form-group">
          <label>Description</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="3"
            placeholder="Enter item description"
          />
        </div>

        <div className="form-group">
          <label>Price *</label>
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
            step="0.01"
            required
            placeholder="0.00"
          />
        </div>

        <div className="form-group">
          <label>Tax</label>
          <input
            type="number"
            name="tax"
            value={formData.tax}
            onChange={handleChange}
            step="0.01"
            placeholder="0.00"
          />
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Creating...' : 'Create Item'}
        </button>
      </form>
    </div>
  )
}

export default ItemForm