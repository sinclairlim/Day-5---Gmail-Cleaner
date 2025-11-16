import { Users, Mail, HardDrive } from 'lucide-react'
import './SenderStats.css'

interface SenderStat {
  sender: string
  count: number
  total_size_mb: number
  email_ids: string[]
}

interface SenderStatsProps {
  senderStats: SenderStat[]
  onSelectSender?: (emailIds: string[]) => void
}

function SenderStats({ senderStats, onSelectSender }: SenderStatsProps) {
  if (!senderStats || senderStats.length === 0) {
    return null
  }

  return (
    <div className="sender-stats">
      <div className="sender-stats-header">
        <Users size={24} />
        <h3>Top Senders</h3>
        <span className="sender-count">({senderStats.length} unique senders)</span>
      </div>

      <div className="sender-list">
        {senderStats.map((stat, index) => (
          <div
            key={index}
            className="sender-item"
            onClick={() => onSelectSender && onSelectSender(stat.email_ids)}
          >
            <div className="sender-rank">#{index + 1}</div>
            <div className="sender-info">
              <div className="sender-email">{stat.sender}</div>
              <div className="sender-details">
                <span className="sender-count-badge">
                  <Mail size={14} />
                  {stat.count} emails
                </span>
                <span className="sender-size-badge">
                  <HardDrive size={14} />
                  {stat.total_size_mb.toFixed(2)} MB
                </span>
              </div>
            </div>
            <div className="sender-actions">
              <span className="select-hint">Click to select all</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default SenderStats
