import { EmailMessage } from '../services/api'
import { Mail, Calendar, User } from 'lucide-react'
import './EmailList.css'

interface EmailListProps {
  emails: EmailMessage[]
  selectedEmails: Set<string>
  onToggleSelection: (emailId: string) => void
}

function EmailList({ emails, selectedEmails, onToggleSelection }: EmailListProps) {
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  const formatSize = (bytes: number) => {
    const mb = bytes / (1024 * 1024)
    if (mb >= 1) {
      return mb.toFixed(2) + ' MB'
    }
    return (bytes / 1024).toFixed(2) + ' KB'
  }

  return (
    <div className="email-list">
      {emails.map((email) => (
        <div
          key={email.id}
          className={`email-item ${selectedEmails.has(email.id) ? 'selected' : ''}`}
          onClick={() => onToggleSelection(email.id)}
        >
          <input
            type="checkbox"
            checked={selectedEmails.has(email.id)}
            onChange={() => onToggleSelection(email.id)}
            className="email-checkbox"
          />

          <div className="email-content">
            <div className="email-subject">
              <Mail size={16} />
              <strong>{email.subject}</strong>
            </div>

            <div className="email-details">
              <span className="email-sender">
                <User size={14} />
                {email.sender}
              </span>
              <span className="email-date">
                <Calendar size={14} />
                {formatDate(email.date)}
              </span>
              <span className="email-size">
                {formatSize(email.size)}
              </span>
            </div>

            <p className="email-snippet">{email.snippet}</p>

            {email.labels.length > 0 && (
              <div className="email-labels">
                {email.labels.slice(0, 3).map((label, idx) => (
                  <span key={idx} className="email-label">{label}</span>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

export default EmailList
