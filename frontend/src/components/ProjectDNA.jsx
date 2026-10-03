import React from 'react';
import { 
  ArrowRight, 
  Cpu, 
  Code, 
  Database, 
  Layers, 
  Layout, 
  Radio, 
  Server, 
  Compass, 
  Sparkles 
} from 'lucide-react';

function getIconForTech(tech = '') {
  const t = tech.toLowerCase();
  if (t.includes('esp') || t.includes('stm') || t.includes('arduino') || t.includes('pico') || t.includes('micro') || t.includes('hardware')) {
    return Cpu;
  }
  if (t.includes('cad') || t.includes('kicad') || t.includes('fusion') || t.includes('solidworks') || t.includes('mech')) {
    return Compass;
  }
  if (t.includes('mqtt') || t.includes('lora') || t.includes('bluetooth') || t.includes('ble') || t.includes('wifi') || t.includes('i2c') || t.includes('spi')) {
    return Radio;
  }
  if (t.includes('sql') || t.includes('db') || t.includes('postgres') || t.includes('redis') || t.includes('mongo')) {
    return Database;
  }
  if (t.includes('fastapi') || t.includes('node') || t.includes('flask') || t.includes('server') || t.includes('backend') || t.includes('ros')) {
    return Server;
  }
  if (t.includes('react') || t.includes('vue') || t.includes('web') || t.includes('dash') || t.includes('ui') || t.includes('frontend')) {
    return Layout;
  }
  return Code;
}

export default function ProjectDNA({ technologies = '', category = 'Embedded', className = '' }) {
  // Parse tech list or provide smart default flow
  let techList = [];
  if (Array.isArray(technologies)) {
    techList = technologies;
  } else if (typeof technologies === 'string' && technologies.trim()) {
    techList = technologies.split(',').map(t => t.trim()).filter(Boolean);
  }

  // If no technologies yet, generate a representative technical stack based on category
  if (techList.length === 0) {
    if (category.toLowerCase().includes('robot')) {
      techList = ['SolidWorks', 'ROS2', 'Arduino', 'Sensors', 'Control Loop'];
    } else if (category.toLowerCase().includes('soft') || category.toLowerCase().includes('web')) {
      techList = ['Architecture', 'FastAPI', 'SQLite', 'REST API', 'React UI'];
    } else {
      techList = ['KiCad', 'ESP32', 'Sensors', 'MQTT', 'Dashboard'];
    }
  }

  return (
    <div className={`panel ${className}`} style={{ padding: '1.5rem', background: 'var(--bg-surface)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Sparkles size={15} color="var(--accent-primary)" />
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-heading)' }}>
              Project DNA
            </h3>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            System technology topology & data lineage
          </p>
        </div>

        <span style={{
          fontSize: '0.72rem',
          fontFamily: 'var(--font-mono)',
          padding: '0.2rem 0.5rem',
          borderRadius: 'var(--radius-xs)',
          background: 'var(--bg-subtle)',
          color: 'var(--text-muted)',
          border: '1px solid var(--border-default)'
        }}>
          {techList.length} LAYERS
        </span>
      </div>

      {/* Visual DNA Flow Sequence */}
      <div className="project-dna-flow">
        {techList.map((tech, idx) => {
          const Icon = getIconForTech(tech);
          const isLast = idx === techList.length - 1;

          return (
            <React.Fragment key={idx}>
              <div className="dna-pill">
                <Icon size={14} color="var(--accent-primary)" />
                <span>{tech}</span>
              </div>

              {!isLast && (
                <div className="dna-arrow">
                  <ArrowRight size={14} />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      <div style={{
        marginTop: '0.85rem',
        fontSize: '0.75rem',
        color: 'var(--text-muted)',
        fontFamily: 'var(--font-mono)',
        display: 'flex',
        alignItems: 'center',
        gap: '0.4rem'
      }}>
        <span>Hardware / Sensor Origin</span>
        <ArrowRight size={11} />
        <span>Telemetry / Bus</span>
        <ArrowRight size={11} />
        <span>Host / Dashboard Surface</span>
      </div>
    </div>
  );
}
