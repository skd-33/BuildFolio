import React from 'react';
import { Lightbulb, Compass, Cpu, Wrench, CheckCircle2, Share2, Check } from 'lucide-react';

const STAGES = [
  { id: 'idea', label: 'Idea', icon: Lightbulb, minProgress: 0, desc: 'Concept definition & feasibility analysis' },
  { id: 'design', label: 'Design', icon: Compass, minProgress: 20, desc: 'Schematics, architecture & CAD modeling' },
  { id: 'prototype', label: 'Prototype', icon: Cpu, minProgress: 40, desc: 'Component breadboarding & initial code' },
  { id: 'build', label: 'Build', icon: Wrench, minProgress: 60, desc: 'PCB fabrication, assembly & core firmware' },
  { id: 'test', label: 'Test', icon: CheckCircle2, minProgress: 80, desc: 'Verification, debugging & calibration' },
  { id: 'publish', label: 'Publish', icon: Share2, minProgress: 100, desc: 'Public portfolio showcase & documentation' }
];

export default function ProjectJourney({ progress = 0, isPublished = false, className = '' }) {
  // Determine active stage
  let activeIndex = 0;
  if (isPublished) {
    activeIndex = 5;
  } else {
    for (let i = STAGES.length - 1; i >= 0; i--) {
      if (progress >= STAGES[i].minProgress) {
        activeIndex = i;
        break;
      }
    }
  }

  const fillPercentage = (activeIndex / (STAGES.length - 1)) * 100;

  return (
    <div className={`panel ${className}`} style={{ padding: '1.5rem', background: 'var(--bg-surface)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-heading)' }}>
            Project Journey
          </h3>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            Engineering lifecycle progression from concept to showcase
          </p>
        </div>

        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.4rem',
          padding: '0.25rem 0.65rem',
          background: 'var(--bg-subtle)',
          borderRadius: 'var(--radius-full)',
          fontSize: '0.75rem',
          fontWeight: 600,
          color: 'var(--accent-primary)',
          border: '1px solid var(--border-default)'
        }}>
          <span>Stage:</span>
          <strong>{STAGES[activeIndex].label}</strong>
        </div>
      </div>

      {/* Visual Timeline Track */}
      <div className="journey-timeline">
        {/* Background track line */}
        <div className="journey-track-line" />
        
        {/* Active progress track fill */}
        <div 
          className="journey-track-fill" 
          style={{ width: `calc(${fillPercentage}% - 24px)` }}
        />

        {STAGES.map((stage, idx) => {
          const isCompleted = isPublished ? true : (idx < activeIndex || (idx === activeIndex && progress === 100));
          const isActive = idx === activeIndex;
          const Icon = stage.icon;

          return (
            <div 
              key={stage.id} 
              className={`journey-node ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}`}
            >
              <div className="journey-dot">
                {isCompleted && !isActive ? (
                  <Check size={14} strokeWidth={3} />
                ) : (
                  <Icon size={14} />
                )}
              </div>
              <span className="journey-label">
                {stage.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* Active Stage Context Note */}
      <div style={{
        marginTop: '0.5rem',
        padding: '0.65rem 0.9rem',
        background: 'var(--bg-subtle)',
        borderRadius: 'var(--radius-sm)',
        fontSize: '0.78rem',
        color: 'var(--text-secondary)',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem'
      }}>
        <span style={{ color: 'var(--accent-primary)', fontWeight: 700 }}>Current Phase:</span>
        <span>{STAGES[activeIndex].desc}</span>
      </div>
    </div>
  );
}
