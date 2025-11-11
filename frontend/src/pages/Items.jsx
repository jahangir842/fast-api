import { useState } from 'react'
import ItemForm from '../components/ItemForm'
import ItemList from '../components/ItemList'

function Items() {
  const [refreshKey, setRefreshKey] = useState(0)

  const handleItemCreated = () => {
    // Trigger refresh of item list
    setRefreshKey(prev => prev + 1)
  }

  return (
    <div>
      <h1 style={{ marginBottom: '2rem' }}>Items Management</h1>
      
      <div style={{ display: 'grid', gap: '2rem' }}>
        <ItemForm onItemCreated={handleItemCreated} />
        <ItemList refresh={refreshKey} />
      </div>
    </div>
  )
}

export default Items