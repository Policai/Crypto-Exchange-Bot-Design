import React from 'react'

const actions = ['Пополнить', 'Вывести', 'Обменять', 'Перевести', 'Создать чек', 'Промокоды', 'Рефералы', 'История операций', 'Поддержка', 'VIP уровень']

export default function App() {
  const user = window?.Telegram?.WebApp?.initDataUnsafe?.user
  return (
    <div className="layout">
      <header className="header">
        <h1>Crypto Exchange</h1>
        <span>@{user?.username || 'guest'}</span>
      </header>
      <section className="card">
        <h2>Баланс</h2>
        <div className="grid">
          {['USDT_TRON','USDT_TON','TON','TRX','BTC','LTC','RUB'].map((asset) => (
            <div key={asset} className="asset">{asset}: 0.00</div>
          ))}
        </div>
      </section>
      <section className="actions">
        {actions.map((action) => (
          <button key={action}>{action}</button>
        ))}
      </section>
    </div>
  )
}
