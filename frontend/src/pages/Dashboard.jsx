import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { projectsApi } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { ProgressBar, Badge } from '../components/UIElements';
import ProjectThumbnail from '../components/ProjectThumbnail';
import { 
  Plus, 
  Search, 
  ExternalLink, 
  Trash2, 
  FileText, 
  ArrowRight,
  Sparkles,
  Calendar,
  DollarSign,
  CheckCircle2,
  Clock,
  Layers,
  Cpu,
  Bot,
  Code
} from 'lucide-react';

export default function Dashboard() {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [deletingId, setDeletingId] = useState(null);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const data = await projectsApi.list();
      setProjects(data || []);
    } catch (err) {
      console.error('Error fetching projects:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleDelete = async (id, name, e) => {
    e.stopPropagation();
    if (window.confirm(`Delete "${name}"? This will permanently remove all tasks, hardware components, and portfolio data.`)) {
      try {
        setDeletingId(id);
        await projectsApi.delete(id);
        setProjects(prev => prev.filter(p => p.id !== id));
      } catch (err) {
        alert('Failed to delete: ' + err.message);
      } finally {
        setDeletingId(null);
      }
    }
  };

  // Metrics
  const totalProjects = projects.length;
  const completedProjects = projects.filter(p => p.progress === 100 || (p.status || '').toLowerCase() === 'completed').length;
  const totalBudget = projects.reduce((acc, p) => acc + (p.budget || 0), 0);
  const totalSpent = projects.reduce((acc, p) => acc + (p.total_spent || 0), 0);

  // Active / Featured Project (first in-progress or highest progress project)
  const featuredProject = projects.length > 0 
    ? [...projects].sort((a, b) => (b.progress || 0) - (a.progress || 0))[0]
    : null;

  // Filtered projects
  const filteredProjects = projects.filter(p => {
    const matchesSearch = 
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      (p.description || '').toLowerCase().includes(search.toLowerCase()) ||
      (p.technologies || '').toLowerCase().includes(search.toLowerCase());

    if (!matchesSearch) return false;
    if (selectedCategory === 'all') return true;

    const cat = (p.category || '').toLowerCase();
    const tech = (p.technologies || '').toLowerCase();
    if (selectedCategory === 'embedded') return cat.includes('embedded') || cat.includes('iot') || tech.includes('esp') || tech.includes('arduino');
    if (selectedCategory === 'robotics') return cat.includes('robot') || tech.includes('ros') || tech.includes('motor');
    if (selectedCategory === 'software') return cat.includes('soft') || cat.includes('web') || tech.includes('react') || tech.includes('python');
    return true;
  });

  return (
    <div className="app-container" style={{ padding: '2.5rem 1.5rem 6rem' }}>
      {/* ─── Welcoming Header ─── */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        flexWrap: 'wrap',
        gap: '1.25rem',
        marginBottom: '2rem'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <span style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.35rem',
              padding: '0.2rem 0.55rem',
              borderRadius: 'var(--radius-full)',
              background: 'var(--accent-primary-subtle)',
              color: 'var(--accent-primary)',
              fontSize: '0.75rem',
              fontWeight: 700,
              letterSpacing: '0.03em',
              textTransform: 'uppercase'
            }}>
              <Sparkles size={13} />
              <span>Studio Workspace</span>
            </span>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              · {totalProjects} Active Build{totalProjects !== 1 ? 's' : ''}
            </span>
          </div>

          <h1 style={{
            fontSize: 'clamp(1.75rem, 3.5vw, 2.3rem)',
            fontWeight: 800,
            color: 'var(--text-heading)',
            letterSpacing: '-0.025em',
            lineHeight: 1.2
          }}>
            Welcome back, {user?.username || 'Maker'}
          </h1>
          <p style={{ fontSize: '0.925rem', color: 'var(--text-secondary)', marginTop: '0.35rem' }}>
            Track your hardware builds, calibrate firmware, and publish standout engineering portfolios.
          </p>
        </div>

        {/* Header Action & Quick Metrics */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', flexWrap: 'wrap' }}>
          <div style={{
            display: 'flex',
            gap: '0.75rem',
            background: 'var(--bg-surface)',
            padding: '0.5rem 0.85rem',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-default)',
            fontSize: '0.8rem'
          }}>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Total Spent: </span>
              <strong style={{ color: 'var(--text-heading)' }}>₹{totalSpent.toFixed(0)}</strong>
            </div>
            <span style={{ color: 'var(--border-strong)' }}>|</span>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Completed: </span>
              <strong style={{ color: 'var(--accent-emerald)' }}>{completedProjects} / {totalProjects}</strong>
            </div>
          </div>

          <Link to="/create" className="btn btn-primary" style={{ gap: '0.45rem' }}>
            <Plus size={16} strokeWidth={2.5} />
            <span>New Project</span>
          </Link>
        </div>
      </div>

      {/* ─── Featured / Spotlight Active Project ─── */}
      {!loading && featuredProject && (
        <div className="featured-card">
          <div className="featured-main">
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                <span style={{
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  textTransform: 'uppercase',
                  color: 'var(--accent-primary)',
                  letterSpacing: '0.04em'
                }}>
                  ● CURRENT FOCUS PROJECT
                </span>
                <Badge status={featuredProject.progress === 100 ? 'Completed' : (featuredProject.status || 'In Progress')} />
                {featuredProject.portfolio?.is_published && (
                  <span className="badge badge-completed">
                    Public Showcase Live
                  </span>
                )}
              </div>

              <h2 style={{
                fontSize: '1.65rem',
                fontWeight: 800,
                color: 'var(--text-heading)',
                marginBottom: '0.5rem',
                letterSpacing: '-0.02em'
              }}>
                {featuredProject.name}
              </h2>

              <p style={{
                fontSize: '0.925rem',
                color: 'var(--text-secondary)',
                lineHeight: 1.6,
                maxWidth: '640px',
                marginBottom: '1.25rem'
              }}>
                {featuredProject.description || 'No description added yet. Set your engineering specs in the project settings.'}
              </p>

              {/* Technologies */}
              {featuredProject.technologies && (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginBottom: '1.5rem' }}>
                  {featuredProject.technologies.split(',').map((tech, idx) => (
                    <span key={idx} className="tech-tag">
                      {tech.trim()}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Progress Meter with Percentage */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem', fontSize: '0.825rem' }}>
                <span style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>Overall Project Progress</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--accent-primary)' }}>
                  {featuredProject.progress}%
                </span>
              </div>
              <ProgressBar progress={featuredProject.progress} height={8} />

              <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1.25rem' }}>
                <Link to={`/project/${featuredProject.id}`} className="btn btn-primary btn-sm" style={{ gap: '0.4rem' }}>
                  <span>Open Workspace</span>
                  <ArrowRight size={14} />
                </Link>

                {featuredProject.portfolio?.is_published && (
                  <Link 
                    to={`/p/${featuredProject.portfolio.slug}`} 
                    target="_blank" 
                    className="btn btn-secondary btn-sm"
                    style={{ gap: '0.4rem', color: 'var(--accent-blue)' }}
                  >
                    <ExternalLink size={13} />
                    <span>View Public Portfolio</span>
                  </Link>
                )}
              </div>
            </div>
          </div>

          {/* Workbench Sidebar Snapshot */}
          <div className="featured-sidebar">
            <div>
              <h3 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-heading)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '1rem' }}>
                Build Snapshot
              </h3>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.825rem' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Tasks Status</span>
                  <span style={{ fontWeight: 600, color: 'var(--text-heading)' }}>
                    {featuredProject.completed_task_count || 0} of {featuredProject.task_count || 0} done
                  </span>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.825rem' }}>
                  <span style={{ color: 'var(--text-muted)' }}>BOM Cost</span>
                  <span style={{ fontWeight: 700, color: featuredProject.total_spent > featuredProject.budget && featuredProject.budget > 0 ? 'var(--status-danger-text)' : 'var(--text-heading)' }}>
                    ₹{featuredProject.total_spent?.toFixed(0) || '0'} 
                    <span style={{ color: 'var(--text-muted)', fontWeight: 400 }}> / ₹{featuredProject.budget?.toFixed(0) || '0'}</span>
                  </span>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.825rem' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Target Deadline</span>
                  <span style={{ fontWeight: 600, color: 'var(--text-heading)' }}>
                    {featuredProject.deadline || 'Flexible'}
                  </span>
                </div>
              </div>
            </div>

            <div style={{
              marginTop: '1.5rem',
              padding: '0.75rem',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--bg-canvas)',
              border: '1px solid var(--border-default)',
              fontSize: '0.78rem',
              color: 'var(--text-secondary)'
            }}>
              <strong style={{ color: 'var(--text-heading)', display: 'block', marginBottom: '0.2rem' }}>
                Quick Tip
              </strong>
              Keep your Bill of Materials updated to catch component cost overruns early before PCB fab.
            </div>
          </div>
        </div>
      )}

      {/* ─── "Your Projects" Section Bar ─── */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '1rem',
        marginBottom: '1.25rem',
        borderBottom: '1px solid var(--border-default)',
        paddingBottom: '1rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-heading)', letterSpacing: '-0.02em' }}>
            All Projects ({filteredProjects.length})
          </h2>

          {/* Category Filter Chips */}
          <div style={{ display: 'flex', gap: '0.4rem' }}>
            <button
              onClick={() => setSelectedCategory('all')}
              className={`btn btn-sm ${selectedCategory === 'all' ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '0.25rem 0.6rem', fontSize: '0.75rem' }}
            >
              All
            </button>
            <button
              onClick={() => setSelectedCategory('embedded')}
              className={`btn btn-sm ${selectedCategory === 'embedded' ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '0.25rem 0.6rem', fontSize: '0.75rem' }}
            >
              IoT & Embedded
            </button>
            <button
              onClick={() => setSelectedCategory('robotics')}
              className={`btn btn-sm ${selectedCategory === 'robotics' ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '0.25rem 0.6rem', fontSize: '0.75rem' }}
            >
              Robotics
            </button>
            <button
              onClick={() => setSelectedCategory('software')}
              className={`btn btn-sm ${selectedCategory === 'software' ? 'btn-primary' : 'btn-secondary'}`}
              style={{ padding: '0.25rem 0.6rem', fontSize: '0.75rem' }}
            >
              Software
            </button>
          </div>
        </div>

        {/* Search Input */}
        <div style={{ position: 'relative', width: '260px' }}>
          <Search size={14} style={{ position: 'absolute', left: '0.85rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input
            type="text"
            className="input-field"
            placeholder="Search projects or tech..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{
              width: '100%',
              paddingLeft: '2.4rem',
              paddingTop: '0.45rem',
              paddingBottom: '0.45rem',
              fontSize: '0.825rem'
            }}
          />
        </div>
      </div>

      {/* ─── Projects Visual Grid ─── */}
      {loading ? (
        <div className="panel" style={{ textAlign: 'center', padding: '4rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          Loading your engineering projects...
        </div>
      ) : filteredProjects.length === 0 ? (
        <div className="panel" style={{ textAlign: 'center', padding: '4rem 1.5rem', background: 'var(--bg-surface)' }}>
          <div style={{
            width: '48px',
            height: '48px',
            borderRadius: '50%',
            background: 'var(--accent-primary-subtle)',
            color: 'var(--accent-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 1rem'
          }}>
            <Cpu size={24} />
          </div>
          <h3 style={{ fontSize: '1.15rem', color: 'var(--text-heading)', marginBottom: '0.4rem', fontWeight: 700 }}>
            {search ? 'No projects match your filter' : 'No projects created yet'}
          </h3>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', maxWidth: '420px', margin: '0 auto 1.5rem', lineHeight: 1.5 }}>
            {search ? 'Try adjusting your search terms or category filter.' : 'Start logging your hardware schematics, firmware tasks, and BOM costs.'}
          </p>
          {!search && (
            <Link to="/create" className="btn btn-primary" style={{ gap: '0.4rem' }}>
              <Plus size={16} />
              <span>Create Your First Project</span>
            </Link>
          )}
        </div>
      ) : (
        <div className="project-grid">
          {filteredProjects.map((p) => {
            const isOver = p.budget > 0 && p.total_spent > p.budget;
            const isPublished = p.portfolio && p.portfolio.is_published;
            const techList = p.technologies ? p.technologies.split(',').map(t => t.trim()).filter(Boolean) : [];

            return (
              <div 
                key={p.id}
                className="project-card"
                onClick={() => window.location.href = `/project/${p.id}`}
                style={{ cursor: 'pointer' }}
              >
                {/* Visual Thumbnail */}
                <ProjectThumbnail project={p} height={105} />

                {/* Body Content */}
                <div className="project-card-body">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.5rem', marginBottom: '0.35rem' }}>
                    <h3 className="project-card-title">
                      {p.name}
                    </h3>
                    <Badge status={p.progress === 100 ? 'Completed' : (p.status || 'In Progress')} />
                  </div>

                  <p className="project-card-desc">
                    {p.description || 'No description provided.'}
                  </p>

                  {/* Tech stack chips */}
                  {techList.length > 0 && (
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem', marginBottom: '1rem' }}>
                      {techList.slice(0, 3).map((tech, idx) => (
                        <span key={idx} className="tech-tag" style={{ fontSize: '0.72rem', padding: '0.15rem 0.45rem' }}>
                          {tech}
                        </span>
                      ))}
                      {techList.length > 3 && (
                        <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', alignSelf: 'center' }}>
                          +{techList.length - 3}
                        </span>
                      )}
                    </div>
                  )}

                  {/* Progress Bar */}
                  <div style={{ marginTop: 'auto', marginBottom: '0.85rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.3rem' }}>
                      <span style={{ color: 'var(--text-muted)' }}>Progress</span>
                      <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--text-heading)' }}>
                        {p.progress}%
                      </span>
                    </div>
                    <ProgressBar progress={p.progress} height={5} />
                  </div>

                  {/* Metadata Row */}
                  <div className="project-card-meta">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                      <CheckCircle2 size={13} color="var(--accent-emerald)" />
                      <span>{p.completed_task_count || 0}/{p.task_count || 0} tasks</span>
                    </div>

                    <div>
                      <span style={{ color: isOver ? 'var(--status-danger-text)' : 'var(--text-heading)', fontWeight: 600 }}>
                        ₹{p.total_spent?.toFixed(0) || '0'}
                      </span>
                      {p.budget > 0 && (
                        <span style={{ color: 'var(--text-muted)' }}> / ₹{p.budget.toFixed(0)}</span>
                      )}
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                      {isPublished ? (
                        <span style={{ fontSize: '0.72rem', color: 'var(--accent-emerald)', fontWeight: 600 }}>
                          Live
                        </span>
                      ) : (
                        <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                          Draft
                        </span>
                      )}

                      <button
                        type="button"
                        onClick={(e) => handleDelete(p.id, p.name, e)}
                        className="btn btn-secondary btn-sm"
                        style={{ padding: '0.2rem 0.35rem', color: 'var(--text-muted)', border: 'none' }}
                        title="Delete project"
                        disabled={deletingId === p.id}
                      >
                        <Trash2 size={12} />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
