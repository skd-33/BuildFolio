import React from 'react';

export function ProgressBar({ progress = 0, showLabel = true, height = 6 }) {
  const clamped = Math.min(100, Math.max(0, Number(progress) || 0));
  const isDone = clamped === 100;

  return (
    <div style={{ width: '100%' }}>
      {showLabel && (
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '0.4rem',
          fontSize: '0.8rem'
        }}>
          <span style={{ color: 'var(--text-muted)', fontWeight: 500 }}>Progress</span>
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontWeight: 600,
            color: isDone ? 'var(--accent-emerald)' : 'var(--text-heading)'
          }}>
            {clamped.toFixed(0)}%
          </span>
        </div>
      )}
      <div className="meter-track" style={{ height }}>
        <div
          className={`meter-fill ${isDone ? 'meter-fill-done' : ''}`}
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  );
}

export function Badge({ status }) {
  const s = (status || '').toLowerCase().trim();

  let className = 'badge-pending';
  let label = status || 'Planning';

  if (s === 'completed') {
    className = 'badge-completed';
    label = 'Completed';
  } else if (s === 'in progress' || s === 'in_progress' || s === 'building') {
    className = 'badge-progress';
    label = 'In Progress';
  } else if (s === 'over-budget' || s === 'danger' || s === 'failed') {
    className = 'badge-danger';
    label = 'Over Budget';
  } else if (s === 'planning') {
    className = 'badge-pending';
    label = 'Planning';
  }

  return (
    <span className={`badge ${className}`}>
      {label}
    </span>
  );
}
