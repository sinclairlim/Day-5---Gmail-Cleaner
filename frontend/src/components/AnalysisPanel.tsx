import { Sparkles } from 'lucide-react'
import './AnalysisPanel.css'

interface AnalysisPanelProps {
  analysis: string
}

function AnalysisPanel({ analysis }: AnalysisPanelProps) {
  return (
    <div className="analysis-panel">
      <div className="analysis-header">
        <Sparkles size={24} />
        <h3>AI Analysis</h3>
      </div>
      <div className="analysis-content">
        {analysis.split('\n').map((line, idx) => (
          <p key={idx}>{line}</p>
        ))}
      </div>
    </div>
  )
}

export default AnalysisPanel
