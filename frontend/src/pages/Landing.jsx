import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ArrowRight, CheckSquare, DollarSign, Link2, FileText } from 'lucide-react';

export default function Landing() {
  const { user } = useAuth();

  return (
    <div style={{ paddingBottom: '6rem' }}>
      {/* Hero Section */}
      <section style={{
        padding: '5rem 0 4rem',
        borderBottom: '1px solid var(--border-default)'
      }}>
        <div className="app-container" style={{ maxWidth: '860px' }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.4rem',
            fontSize: '0.8rem',
            fontWeight: 600,
            color: 'var(--accent-primary)',
            marginBottom: '1.25rem'
          }}>
            <span className="brand-dot" style={{ width: 6, height: 6 }} />
            <span>BuildFolio</span>
          </div>

          <h1 style={{
            fontSize: 'clamp(2.2rem, 4.5vw, 3.2rem)',
            fontWeight: 800,
            lineHeight: 1.12,
            letterSpacing: '-0.03em',
            color: 'var(--text-heading)',
            marginBottom: '1.25rem'
          }}>
            Build, track, and{' '}
            <span style={{ color: 'var(--accent-primary)' }}>showcase</span>{' '}
            your engineering projects
          </h1>

          <p style={{
            fontSize: '1.15rem',
            color: 'var(--text-secondary)',
            lineHeight: 1.65,
            maxWidth: '640px',
            marginBottom: '2rem'
          }}>
            The workspace built for engineering students and hardware makers.
            Track tasks, manage your bill of materials in ₹, and publish beautiful
            project portfolios — all in one place.
          </p>

          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            {user ? (
              <Link to="/dashboard" className="btn btn-primary" style={{ padding: '0.65rem 1.5rem' }}>
                <span>Go to Dashboard</span>
                <ArrowRight size={16} />
              </Link>
            ) : (
              <>
                <Link to="/signup" className="btn btn-primary" style={{ padding: '0.65rem 1.5rem' }}>
                  <span>Get Started — Free</span>
                  <ArrowRight size={16} />
                </Link>
                <Link to="/login" className="btn btn-secondary" style={{ padding: '0.65rem 1.25rem' }}>
                  <span>Sign In</span>
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="app-container" style={{ maxWidth: '960px', marginTop: '4rem' }}>
        <h2 style={{
          fontSize: '0.85rem',
          fontWeight: 700,
          color: 'var(--text-muted)',
          textTransform: 'uppercase',
          letterSpacing: '0.06em',
          marginBottom: '1.5rem',
          paddingBottom: '0.6rem',
          borderBottom: '1px solid var(--border-default)'
        }}>
          Everything you need to ship great projects
        </h2>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
          gap: '1.25rem'
        }}>
          <div className="panel">
            <div className="panel-header">
              <span className="panel-title">Task Tracking</span>
              <CheckSquare size={16} color="var(--accent-blue)" />
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.65 }}>
              Break your project into milestones. Track status, see completion percentage update in real time as you check off tasks.
            </p>
          </div>

          <div className="panel">
            <div className="panel-header">
              <span className="panel-title">Bill of Materials</span>
              <DollarSign size={16} color="var(--accent-primary)" />
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.65 }}>
              Log every component in Indian Rupees (₹). Automatic cost calculations, 80% budget warnings, and CSV export for your records.
            </p>
          </div>

          <div className="panel">
            <div className="panel-header">
              <span className="panel-title">Project Links</span>
              <Link2 size={16} color="var(--text-muted)" />
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.65 }}>
              Attach your GitHub repo, KiCad schematics, Fusion 360 models, and documentation links. Everything in one place.
            </p>
          </div>

          <div className="panel">
            <div className="panel-header">
              <span className="panel-title">Portfolio & Showcase</span>
              <FileText size={16} color="var(--accent-emerald)" />
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.65 }}>
              Generate a public project page with a custom URL. Write your problem statement, solution, and share it with anyone — no login needed.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
