export default function EvidencePanel({ claim, evidence, riskScore }) {
  if (!claim) {
    return (
      <div className="bg-gray-700 rounded-lg p-8 text-center">
        <svg className="w-16 h-16 mx-auto text-gray-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
        <p className="text-gray-400">Select a claim to view evidence</p>
        <p className="text-sm text-gray-500 mt-2">External verification data will appear here</p>
      </div>
    );
  }

  const claimEvidence = evidence.filter(e => e.claim_id === claim.claim_id);

  const getSignalIcon = (signalType) => {
    switch (signalType) {
      case 'thermal_anomaly':
        return '🔥';
      case 'negative_news':
        return '📰';
      case 'no_anomaly':
        return '✅';
      case 'neutral_news':
        return '📄';
      default:
        return '📊';
    }
  };

  const getSignalColor = (signalType) => {
    switch (signalType) {
      case 'thermal_anomaly':
      case 'negative_news':
        return 'border-red-500 bg-red-900 bg-opacity-20';
      case 'no_anomaly':
      case 'neutral_news':
        return 'border-green-500 bg-green-900 bg-opacity-20';
      default:
        return 'border-gray-500 bg-gray-700';
    }
  };

  return (
    <div className="space-y-4">
      {/* Claim Summary */}
      <div className="bg-gray-700 p-4 rounded-lg">
        <h3 className="font-semibold text-sm mb-2">Selected Claim</h3>
        <p className="text-sm text-gray-300">{claim.claim_text}</p>
        {claim.value && (
          <p className="text-lg font-bold text-blue-400 mt-2">
            {claim.value}{claim.unit} {claim.year && `(${claim.year})`}
          </p>
        )}
      </div>

      {/* Map Placeholder */}
      <div className="bg-gray-700 rounded-lg h-64 flex flex-col items-center justify-center">
        <svg className="w-12 h-12 text-gray-500 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
        </svg>
        <p className="text-gray-400 text-sm">Facility Location Map</p>
        <p className="text-xs text-gray-500 mt-1">
          {claim.facility_name || 'Location data pending'}
        </p>
      </div>

      {/* Evidence Cards */}
      <div className="space-y-2">
        <h3 className="font-semibold text-sm">External Evidence</h3>
        
        {claimEvidence.length === 0 ? (
          <div className="bg-gray-700 p-4 rounded-lg text-center">
            <p className="text-sm text-gray-400">Loading evidence...</p>
          </div>
        ) : (
          claimEvidence.map((ev) => (
            <div
              key={ev.evidence_id}
              className={`border-2 p-3 rounded-lg ${getSignalColor(ev.signal_type)}`}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-xl">{getSignalIcon(ev.signal_type)}</span>
                  <span className="text-xs font-semibold text-gray-300">{ev.source}</span>
                </div>
                <span className="text-xs bg-gray-800 px-2 py-1 rounded">
                  Strength: {(ev.signal_strength * 100).toFixed(0)}%
                </span>
              </div>
              <p className="text-sm text-gray-200">{ev.signal_text}</p>
              <p className="text-xs text-gray-400 mt-1">
                {new Date(ev.timestamp).toLocaleDateString()}
              </p>
            </div>
          ))
        )}
      </div>

      {/* AI Explanation */}
      {riskScore && (
        <div className="bg-gradient-to-br from-blue-900 to-purple-900 p-4 rounded-lg border border-blue-500">
          <div className="flex items-center gap-2 mb-3">
            <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <h3 className="font-semibold text-sm">AI Analysis</h3>
          </div>
          <div className="text-sm text-gray-200 whitespace-pre-line">
            {riskScore.reasoning}
          </div>
        </div>
      )}
    </div>
  );
}

// Made with Bob
