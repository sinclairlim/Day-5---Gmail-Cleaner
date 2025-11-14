import { ReactNode } from 'react'
import './StatsCard.css'

interface StatsCardProps {
  title: string
  value: string | number
  icon: ReactNode
}

function StatsCard({ title, value, icon }: StatsCardProps) {
  return (
    <div className="stats-card">
      <div className="stats-icon">{icon}</div>
      <div className="stats-info">
        <h3>{title}</h3>
        <p className="stats-value">{value}</p>
      </div>
    </div>
  )
}

export default StatsCard
