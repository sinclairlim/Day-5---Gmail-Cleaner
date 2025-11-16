import { useState, useEffect } from 'react'
import { logout, scanEmails, deleteEmails, getStats, EmailMessage, ScanResult, Stats } from '../services/api'
import { Mail, LogOut, Trash2, Search, BarChart3 } from 'lucide-react'
import EmailList from '../components/EmailList'
import StatsCard from '../components/StatsCard'
import AnalysisPanel from '../components/AnalysisPanel'
import SenderStats from '../components/SenderStats'
import './DashboardPage.css'

interface DashboardPageProps {
  onLogout: () => void
}

function DashboardPage({ onLogout }: DashboardPageProps) {
  const [loading, setLoading] = useState(false)
  const [scanResult, setScanResult] = useState<ScanResult | null>(null)
  const [selectedEmails, setSelectedEmails] = useState<Set<string>>(new Set())
  const [stats, setStats] = useState<Stats | null>(null)
  const [maxResults, setMaxResults] = useState(5000)
  const [progress, setProgress] = useState(0)
  const [scanStatus, setScanStatus] = useState('')

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const data = await getStats()
      setStats(data)
    } catch (error) {
      console.error('Failed to load stats:', error)
    }
  }

  const handleScan = async () => {
    setLoading(true)
    setSelectedEmails(new Set())
    setProgress(0)
    setScanStatus('Starting scan...')

    // Estimate progress based on expected time
    // ~1 second per 50 emails (batch)
    const estimatedSeconds = Math.ceil(maxResults / 50)
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 95) return prev // Cap at 95% until actually done
        return prev + (100 / estimatedSeconds)
      })
    }, 1000)

    try {
      setScanStatus(`Scanning ${maxResults} emails...`)
      const result = await scanEmails('inbox', maxResults)
      clearInterval(progressInterval)
      setProgress(100)
      setScanStatus('Scan complete!')
      setScanResult(result)
      setTimeout(() => {
        setProgress(0)
        setScanStatus('')
      }, 2000)
    } catch (error) {
      clearInterval(progressInterval)
      setProgress(0)
      setScanStatus('')
      console.error('Scan failed:', error)
      alert('Scan failed. Please try again.')
    }
    setLoading(false)
  }

  const handleDelete = async () => {
    if (selectedEmails.size === 0) {
      alert('Please select emails to delete')
      return
    }

    if (!confirm(`Are you sure you want to delete ${selectedEmails.size} email(s)?`)) {
      return
    }

    setLoading(true)
    try {
      const result = await deleteEmails(Array.from(selectedEmails))
      alert(result.message)

      // Refresh scan results
      if (scanResult) {
        const updatedEmails = scanResult.emails.filter(e => !selectedEmails.has(e.id))
        setScanResult({
          ...scanResult,
          emails: updatedEmails,
          total_count: updatedEmails.length,
          total_size_mb: updatedEmails.reduce((sum, e) => sum + e.size, 0) / (1024 * 1024)
        })
      }

      setSelectedEmails(new Set())
      loadStats()
    } catch (error) {
      console.error('Delete failed:', error)
      alert('Delete failed. Please try again.')
    }
    setLoading(false)
  }

  const handleLogout = async () => {
    try {
      await logout()
      onLogout()
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  const toggleEmailSelection = (emailId: string) => {
    const newSelection = new Set(selectedEmails)
    if (newSelection.has(emailId)) {
      newSelection.delete(emailId)
    } else {
      newSelection.add(emailId)
    }
    setSelectedEmails(newSelection)
  }

  const selectAll = () => {
    if (scanResult) {
      setSelectedEmails(new Set(scanResult.emails.map(e => e.id)))
    }
  }

  const deselectAll = () => {
    setSelectedEmails(new Set())
  }

  const selectEmailsFromSender = (emailIds: string[]) => {
    setSelectedEmails(new Set(emailIds))
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <div className="logo">
            <Mail size={32} />
            <h1>Gmail Cleaner</h1>
          </div>
          <button className="logout-button" onClick={handleLogout}>
            <LogOut size={20} />
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard-content">
        {stats && (
          <div className="stats-grid">
            <StatsCard
              title="Total Emails"
              value={stats.total_emails}
              icon={<Mail size={24} />}
            />
            <StatsCard
              title="Total Size"
              value={`${stats.total_size_mb.toFixed(2)} MB`}
              icon={<BarChart3 size={24} />}
            />
            <StatsCard
              title="Spam Emails"
              value={stats.spam_count}
              icon={<Trash2 size={24} />}
            />
          </div>
        )}

        <div className="scan-section">
          <h2>Scan Your Inbox (Sorted by Size)</h2>
          <div className="scan-controls">
            <input
              type="number"
              value={maxResults}
              onChange={(e) => setMaxResults(parseInt(e.target.value))}
              min="100"
              max="50000"
              step="100"
              className="max-results-input"
              placeholder="Number of emails to scan"
            />

            <button
              className="scan-button"
              onClick={handleScan}
              disabled={loading}
            >
              <Search size={20} />
              {loading ? 'Scanning...' : 'Scan Emails'}
            </button>
          </div>

          {loading && (
            <div style={{ marginTop: '1rem' }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                marginBottom: '0.5rem',
                fontSize: '0.875rem',
                color: '#4a5568'
              }}>
                <span>{scanStatus}</span>
                <span>{Math.round(progress)}%</span>
              </div>
              <div style={{
                width: '100%',
                height: '8px',
                backgroundColor: '#e2e8f0',
                borderRadius: '4px',
                overflow: 'hidden'
              }}>
                <div style={{
                  width: `${progress}%`,
                  height: '100%',
                  backgroundColor: '#667eea',
                  transition: 'width 0.3s ease',
                  borderRadius: '4px'
                }} />
              </div>
              <p style={{ fontSize: '0.75rem', color: '#718096', marginTop: '0.5rem' }}>
                Estimated time: ~{Math.ceil(maxResults / 50)} seconds
              </p>
            </div>
          )}

          {!loading && (
            <p style={{ fontSize: '0.875rem', color: '#718096', marginTop: '0.5rem' }}>
              Scans your entire inbox and sorts by email size (largest first)
            </p>
          )}
        </div>

        {scanResult && (
          <>
            <AnalysisPanel analysis={scanResult.analysis} />

            <SenderStats
              senderStats={scanResult.sender_stats}
              onSelectSender={selectEmailsFromSender}
            />

            <div className="results-section">
              <div className="results-header">
                <h2>
                  Found {scanResult.total_count} emails
                  ({scanResult.total_size_mb.toFixed(2)} MB)
                </h2>
                <div className="results-actions">
                  <button onClick={selectAll} className="action-button">
                    Select All
                  </button>
                  <button onClick={deselectAll} className="action-button">
                    Deselect All
                  </button>
                  <button
                    onClick={handleDelete}
                    className="delete-button"
                    disabled={selectedEmails.size === 0 || loading}
                  >
                    <Trash2 size={20} />
                    Delete Selected ({selectedEmails.size})
                  </button>
                </div>
              </div>

              <EmailList
                emails={scanResult.emails}
                selectedEmails={selectedEmails}
                onToggleSelection={toggleEmailSelection}
              />
            </div>
          </>
        )}
      </main>
    </div>
  )
}

export default DashboardPage
