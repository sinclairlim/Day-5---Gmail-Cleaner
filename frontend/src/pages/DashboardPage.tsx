import { useState } from 'react'
import { logout, scanEmails, deleteEmails, getScanProgress, ScanResult } from '../services/api'
import { Mail, LogOut, Trash2, Search } from 'lucide-react'
import EmailList from '../components/EmailList'
import SenderStats from '../components/SenderStats'
import './DashboardPage.css'

interface DashboardPageProps {
  onLogout: () => void
}

function DashboardPage({ onLogout }: DashboardPageProps) {
  const [loading, setLoading] = useState(false)
  const [scanResult, setScanResult] = useState<ScanResult | null>(null)
  const [selectedEmails, setSelectedEmails] = useState<Set<string>>(new Set())
  const [maxResults, setMaxResults] = useState(5000)

  const handleScan = async () => {
    setLoading(true)
    setSelectedEmails(new Set())

    // Start polling IMMEDIATELY at high frequency
    const progressInterval = setInterval(async () => {
      try {
        const progressData = await getScanProgress()
        console.log('Progress update:', progressData) // Debug log
        // Only update if not "No scan in progress"
        if (progressData.status !== 'No scan in progress') {
          // status updates disabled for now
        }
      } catch (error) {
        console.error('Failed to get progress:', error)
      }
    }, 100) // Poll every 100ms for very responsive updates

    // Tiny delay to ensure interval starts
    await new Promise(resolve => setTimeout(resolve, 50))

    try {
      const result = await scanEmails('inbox', maxResults)
      clearInterval(progressInterval)
      setScanResult(result)
    } catch (error) {
      clearInterval(progressInterval)
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
        {/* Stats disabled to avoid automatic API calls */}
        {/* {stats && (
          <div className="stats-grid">
            <StatsCard
              title="Large Emails"
              value={stats.large_emails_count}
              icon={<Mail size={24} />}
            />
            <StatsCard
              title="Total Size"
              value={`${stats.total_size_mb.toFixed(2)} MB`}
              icon={<BarChart3 size={24} />}
            />
            <StatsCard
              title="Avg Size"
              value={stats.large_emails_count > 0 ? `${(stats.total_size_mb / stats.large_emails_count).toFixed(2)} MB` : '0 MB'}
              icon={<BarChart3 size={24} />}
            />
          </div>
        )} */}

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

          <p style={{ fontSize: '0.875rem', color: '#718096', marginTop: '0.5rem' }}>
            Scans your entire inbox and sorts by email size (largest first)
          </p>
          <p style={{ fontSize: '0.875rem', color: '#718096', marginTop: '0.25rem', fontStyle: 'italic' }}>
            Estimated time: ~10s (100 emails) • ~50s (500 emails) • ~100s (1000 emails)
          </p>
        </div>

        {scanResult && (
          <>
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
