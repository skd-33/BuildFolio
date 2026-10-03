import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { publicApi } from '../api/client';
import { Badge } from '../components/UIElements';
import ProjectJourney from '../components/ProjectJourney';
import ProjectDNA from '../components/ProjectDNA';
import { 
  ExternalLink, 
  Cpu, 
  Calendar, 
  User, 
  FileText, 
  Compass, 
  Code,
  Share2,
  Sparkles,
  CheckCircle2,
  Layers,
  ArrowRight,
  ShieldCheck
} from 'lucide-react';

export default function PublicPortfolio() {
  const { slug } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchShowcase() {
      try {
        setLoading(true);
        const res = await publicApi.getPortfolio(slug);
        setData(res);
      } catch (err) {
        setError(err.message || 'Project portfolio is currently unpublished or does not exist');
      } finally {
        setLoading(false);
      }
    }
    fetchShowcase();
  }, [slug]);

  if (loading) {
    return (
      <div style={{
        minHeight: '75vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '0.95rem',
        color: 'var(--text-muted)'
      }}>
        Loading technical project portfolio...
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="app-container" style={{ padding: '8rem 1.5rem', textAlign: 'center' }}>
        <div style={{
          width: '54px',
          height: '54px',
          borderRadius: '50%',
          background: 'var(--bg-subtle)',
          color: 'var(--text-muted)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 1.25rem'
        }}>
          <FileText size={24} />
        </div>
        <h2 style={{ fontSize: '1.85rem', fontWeight: 800, color: 'var(--text-heading)', marginBottom: '0.75rem' }}>
          Portfolio Unavailable
        </h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '460px', margin: '0 auto 2rem', fontSize: '0.95rem', lineHeight: 1.6 }}>
          {error || 'This project showcase is currently unpublished, private, or does not exist.'}
        </p>
        <Link to="/" className="btn btn-secondary">
          Explore ProjectPulse
        </Link>
      </div>
    );
  }

  const techList = data.technologies 
    ? data.technologies.split(',').map(t => t.trim()).filter(Boolean)
    : [];

  const formattedDate = data.published_at 
    ? new Date(data.published_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
    : 'Published Showcase';

  return (
    <div style={{ minHeight: '100vh', paddingBottom: '8rem' }}>
      {/* ─── Premium Editorial Case Study Masthead ─── */}
      <header style={{
        borderBottom: '1px solid var(--border-default)',
        background: 'var(--bg-surface)',
        padding: '4.5rem 0 3.5rem',
        transition: 'background-color var(--transition-base)'
      }}>
        <div className="app-container" style={{ maxWidth: '920px' }}>
          {/* Top Publication Meta Bar */}
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontSize: '0.8rem',
            color: 'var(--text-muted)',
            marginBottom: '1.75rem',
            flexWrap: 'wrap',
            gap: '0.75rem',
            paddingBottom: '0.75rem',
            borderBottom: '1px solid var(--border-default)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '0.75rem',
                color: 'var(--accent-primary)',
                background: 'var(--accent-primary-subtle)',
                padding: '0.15rem 0.5rem',
                borderRadius: 'var(--radius-xs)',
                fontWeight: 700
              }}>
                CASE STUDY
              </span>
              <span>/p/{slug}</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <Calendar size={13} />
              <span>{formattedDate}</span>
            </div>
          </div>

          {/* Project Title (Hero Typography) */}
          <h1 style={{
            fontSize: 'clamp(2.4rem, 5vw, 3.4rem)',
            fontWeight: 800,
            lineHeight: 1.15,
            letterSpacing: '-0.03em',
            color: 'var(--text-heading)',
            marginBottom: '1.25rem'
          }}>
            {data.title || data.project_name}
          </h1>

          {/* Subtitle / Scope */}
          {data.subtitle && (
            <p style={{
              fontSize: '1.2rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.6,
              marginBottom: '2.25rem',
              maxWidth: '820px'
            }}>
              {data.subtitle}
            </p>
          )}

          {/* Author Byline & Core Highlights */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
            gap: '1rem',
            marginBottom: '2rem'
          }}>
            <div className="metric-card" style={{ padding: '0.85rem 1.1rem' }}>
              <span className="metric-label">Created By</span>
              <div style={{ fontWeight: 700, color: 'var(--text-heading)', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '1rem' }}>
                <User size={15} color="var(--accent-primary)" />
                <span>{data.author_display_name || data.author_username}</span>
              </div>
            </div>

            <div className="metric-card" style={{ padding: '0.85rem 1.1rem' }}>
              <span className="metric-label">Build Status</span>
              <div style={{ marginTop: '0.3rem' }}>
                <Badge status={data.status || 'Completed'} />
              </div>
            </div>

            <div className="metric-card" style={{ padding: '0.85rem 1.1rem' }}>
              <span className="metric-label">Hardware Investment</span>
              <div style={{ fontWeight: 800, color: 'var(--text-heading)', marginTop: '0.25rem', fontSize: '1.1rem' }}>
                ₹{data.total_spent.toFixed(2)}
              </div>
            </div>

            <div className="metric-card" style={{ padding: '0.85rem 1.1rem' }}>
              <span className="metric-label">Milestones Completed</span>
              <div style={{ fontWeight: 800, color: 'var(--accent-emerald)', marginTop: '0.25rem', fontSize: '1.1rem' }}>
                {data.progress_percentage.toFixed(0)}%
              </div>
            </div>
          </div>

          {/* Technology Stack Tags */}
          {techList.length > 0 && (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '2rem' }}>
              {techList.map((tech, idx) => (
                <span key={idx} className="tech-tag" style={{ fontSize: '0.8rem', padding: '0.25rem 0.75rem' }}>
                  {tech}
                </span>
              ))}
            </div>
          )}

          {/* External Artifact Anchors */}
          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            {data.github_url && (
              <a
                href={data.github_url}
                target="_blank"
                rel="noreferrer"
                className="btn btn-secondary btn-sm"
                style={{ gap: '0.45rem' }}
              >
                <Code size={14} color="var(--accent-blue)" />
                <span>GitHub Source</span>
                <ExternalLink size={11} />
              </a>
            )}
            {data.kicad_url && (
              <a
                href={data.kicad_url}
                target="_blank"
                rel="noreferrer"
                className="btn btn-secondary btn-sm"
                style={{ gap: '0.45rem' }}
              >
                <Cpu size={14} color="var(--accent-primary)" />
                <span>KiCad Schematics</span>
                <ExternalLink size={11} />
              </a>
            )}
            {data.fusion_url && (
              <a
                href={data.fusion_url}
                target="_blank"
                rel="noreferrer"
                className="btn btn-secondary btn-sm"
                style={{ gap: '0.45rem' }}
              >
                <Compass size={14} color="var(--accent-blue)" />
                <span>3D CAD Model</span>
                <ExternalLink size={11} />
              </a>
            )}
            {data.docs_url && (
              <a
                href={data.docs_url}
                target="_blank"
                rel="noreferrer"
                className="btn btn-secondary btn-sm"
                style={{ gap: '0.45rem' }}
              >
                <FileText size={14} color="var(--text-muted)" />
                <span>Documentation</span>
                <ExternalLink size={11} />
              </a>
            )}
          </div>
        </div>
      </header>

      {/* ─── Case Study Core Editorial Body ─── */}
      <main className="app-container" style={{ maxWidth: '920px', marginTop: '3.5rem' }}>
        {/* Project Journey Lifecycle Timeline */}
        <section style={{ marginBottom: '3rem' }}>
          <ProjectJourney 
            progress={data.progress_percentage || 100} 
            isPublished={true} 
          />
        </section>

        {/* SECTION 1: THE CHALLENGE & PROBLEM */}
        <section className="panel" style={{ marginBottom: '2.5rem', padding: '2.25rem' }}>
          <div className="panel-header">
            <span className="panel-title" style={{ fontSize: '1.05rem' }}>
              The Problem & Engineering Challenge
            </span>
          </div>
          <p style={{
            color: 'var(--text-primary)',
            lineHeight: 1.8,
            fontSize: '1rem',
            whiteSpace: 'pre-wrap'
          }}>
            {data.problem || data.project_description || 'Problem statement pending author documentation.'}
          </p>
        </section>

        {/* SECTION 2: THE SOLUTION */}
        <section className="panel" style={{ marginBottom: '2.5rem', padding: '2.25rem' }}>
          <div className="panel-header">
            <span className="panel-title" style={{ fontSize: '1.05rem' }}>
              Solution Architecture & Implementation
            </span>
          </div>
          <p style={{
            color: 'var(--text-primary)',
            lineHeight: 1.8,
            fontSize: '1rem',
            whiteSpace: 'pre-wrap'
          }}>
            {data.solution || 'Implementation highlights pending author documentation.'}
          </p>
        </section>

        {/* Project DNA System Topology */}
        <section style={{ marginBottom: '2.5rem' }}>
          <ProjectDNA 
            technologies={data.technologies || ''} 
            category="Embedded" 
          />
        </section>

        {/* SECTION 3: SYSTEM TOPOLOGY & SIGNAL FLOW */}
        {data.architecture_data && (
          <section className="panel" style={{ marginBottom: '2.5rem', padding: '2.25rem' }}>
            <div className="panel-header">
              <span className="panel-title" style={{ fontSize: '1.05rem' }}>
                System Architecture & Data Flow
              </span>
            </div>
            <div style={{
              background: 'var(--bg-subtle)',
              border: '1px solid var(--border-default)',
              borderRadius: 'var(--radius-sm)',
              padding: '1.5rem',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.875rem',
              color: 'var(--text-primary)',
              lineHeight: 1.65,
              whiteSpace: 'pre-wrap'
            }}>
              {data.architecture_data}
            </div>
          </section>
        )}

        {/* SECTION 4: HARDWARE PROCUREMENT (BOM) */}
        <section className="panel" style={{ marginBottom: '3.5rem', padding: '2.25rem' }}>
          <div className="panel-header">
            <span className="panel-title" style={{ fontSize: '1.05rem' }}>
              Hardware Bill of Materials (BOM)
            </span>
            <span style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-heading)' }}>
              Total: ₹{data.total_spent.toFixed(2)} INR
            </span>
          </div>

          <p style={{ fontSize: '0.925rem', color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.6 }}>
            Comprehensive hardware audit and component sourcing for this build. Total procurement expenditure stands at <strong>₹{data.total_spent.toFixed(2)}</strong> across {data.component_count} components.
          </p>

          <div style={{
            padding: '1.1rem 1.4rem',
            background: 'var(--bg-subtle)',
            border: '1px solid var(--border-default)',
            borderRadius: 'var(--radius-sm)',
            fontSize: '0.875rem',
            color: 'var(--text-secondary)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '1rem'
          }}>
            <span>Logged Components: <strong style={{ color: 'var(--text-heading)' }}>{data.component_count} Items</strong></span>
            <span>Total Expenditure: <strong style={{ color: 'var(--text-heading)' }}>₹{data.total_spent.toFixed(2)} INR</strong></span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              <ShieldCheck size={16} color="var(--accent-emerald)" />
              <strong style={{ color: 'var(--accent-emerald)' }}>Verified Build</strong>
            </span>
          </div>
        </section>

        {/* ─── Editorial Publication Footer ─── */}
        <footer style={{
          borderTop: '1px solid var(--border-default)',
          paddingTop: '3rem',
          textAlign: 'center',
          fontSize: '0.875rem',
          color: 'var(--text-muted)'
        }}>
          <div style={{ fontWeight: 600, color: 'var(--text-heading)' }}>
            Published with{' '}
            <Link to="/" style={{ color: 'var(--accent-primary)', textDecoration: 'none' }}>
              ProjectPulse 2.0
            </Link>
          </div>
          <div style={{ marginTop: '0.4rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            The Modern Technical Project Workspace & Showcase for Engineers and Makers
          </div>
        </footer>
      </main>
    </div>
  );
}
