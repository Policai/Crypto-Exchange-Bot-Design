import React from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'

function App(){
  return <div className='wrap'><h1>Admin Panel</h1><p>Комиссии, лимиты, VIP, промокоды, чеки, модераторы.</p></div>
}
createRoot(document.getElementById('root')).render(<App/>)
