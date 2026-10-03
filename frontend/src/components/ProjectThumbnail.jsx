import React from 'react';
import { Cpu, Layers, Code, Compass, Bot, Radio, Wrench } from 'lucide-react';

export default function ProjectThumbnail({ project, height = 120 }) {
  const name = project?.name || 'Project';
  const category = (project?.category || '').toLowerCase();
  const tech = (project?.technologies || '').toLowerCase();

  // Determine theme style
  let styleClass = 'project-thumb-default';
  let Icon = Cpu;
  let label = 'Hardware Build';

  if (category.includes('robot') || tech.includes('ros') || tech.includes('motor')) {
    styleClass = 'project-thumb-robotics';
    Icon = Bot;
    label = 'Robotics & Control';
  } else if (category.includes('soft') || category.includes('web') || tech.includes('react') || tech.includes('fastapi')) {
    styleClass = 'project-thumb-software';
    Icon = Code;
    label = 'Software Architecture';
  } else if (category.includes('iot') || tech.includes('esp') || tech.includes('lora') || tech.includes('sensor')) {
    styleClass = 'project-thumb-embedded';
    Icon = Radio;
    label = 'IoT & Telemetry';
  } else if (tech.includes('cad') || tech.includes('kicad')) {
    styleClass = 'project-thumb-embedded';
    Icon = Compass;
    label = 'Schematic & CAD';
  }

  // Generate subtle unique hash for geometric variation
  const hash = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  const rotation = (hash % 30) - 15;

  return (
    <div 
      className={`project-thumb ${styleClass}`}
      style={{ height: `${height}px` }}
    >
      {/* Abstract technical blueprint geometric accents */}
      <svg 
        style={{ 
          position: 'absolute', 
          top: 0, 
          right: 0, 
          width: '180px', 
          height: '100%', 
          opacity: 0.18, 
          pointerEvents: 'none' 
        }} 
        viewBox="0 0 200 120"
      >
        <circle cx="150" cy="50" r="40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeDasharray="4 4" />
        <line x1="80" y1="20" x2="160" y2="100" stroke="currentColor" strokeWidth="1" />
        <rect x="130" y="30" width="40" height="40" fill="none" stroke="currentColor" strokeWidth="1" transform={`rotate(${rotation} 150 50)`} />
        <circle cx="150" cy="50" r="4" fill="currentColor" />
        <circle cx="110" cy="90" r="3" fill="currentColor" />
      </svg>

      <div className="project-thumb-content">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <div className="project-thumb-icon">
            <Icon size={18} color="var(--accent-primary)" />
          </div>
          <span style={{
            fontSize: '0.75rem',
            fontWeight: 700,
            letterSpacing: '0.02em',
            color: 'var(--text-heading)',
            textShadow: '0 1px 2px rgba(0,0,0,0.4)',
            background: 'var(--bg-surface)',
            padding: '0.2rem 0.5rem',
            borderRadius: 'var(--radius-xs)',
            border: '1px solid var(--border-default)'
          }}>
            {label}
          </span>
        </div>

        {/* Small build code */}
        <span style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.7rem',
          color: 'var(--text-muted)',
          background: 'var(--bg-surface)',
          padding: '0.15rem 0.45rem',
          borderRadius: 'var(--radius-xs)',
          border: '1px solid var(--border-default)'
        }}>
          #{String(project?.id || 1).padStart(3, '0')}
        </span>
      </div>
    </div>
  );
}
