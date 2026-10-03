import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { 
  projectsApi, 
  tasksApi, 
  componentsApi, 
  portfolioApi 
} from '../api/client';
import { ProgressBar, Badge } from '../components/UIElements';
import ProjectJourney from '../components/ProjectJourney';
import ProjectDNA from '../components/ProjectDNA';
import { 
  ArrowLeft, 
  CheckCircle2, 
  Circle, 
  Plus, 
  Trash2, 
  Download, 
  ExternalLink, 
  AlertTriangle, 
  FileText, 
  Settings, 
  Check, 
  Copy, 
  Cpu, 
  Compass, 
  Code,
  Share2,
  Calendar,
  DollarSign,
  ListTodo,
  Layers,
  FolderGit2,
  Activity,
  ArrowRight,
  Sparkles,
  Edit2
} from 'lucide-react';

export default function ProjectWorkspace() {
  const { id } = useParams();
  const navigate = useNavigate();
  const projectId = parseInt(id, 10);

  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [components, setComponents] = useState([]);
  const [costs, setCosts] = useState(null);
  const [portfolio, setPortfolio] = useState(null);

  // Six defined workspace tabs: overview, tasks, hardware, files, portfolio, settings
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // New task state
  const [newTaskName, setNewTaskName] = useState('');
  const [newTaskDesc, setNewTaskDesc] = useState('');
  const [addingTask, setAddingTask] = useState(false);

  // New component state
  const [showAddComp, setShowAddComp] = useState(false);
  const [compName, setCompName] = useState('');
  const [compCategory, setCompCategory] = useState('MCU');
  const [compQty, setCompQty] = useState(1);
  const [compPrice, setCompPrice] = useState('');
  const [compLink, setCompLink] = useState('');
  const [compNotes, setCompNotes] = useState('');

  // Edit component state
  const [editingCompId, setEditingCompId] = useState(null);
  const [editCompName, setEditCompName] = useState('');
  const [editCompCategory, setEditCompCategory] = useState('');
  const [editCompQty, setEditCompQty] = useState(1);
  const [editCompPrice, setEditCompPrice] = useState('');
  const [editCompLink, setEditCompLink] = useState('');
  const [editCompNotes, setEditCompNotes] = useState('');

  // Portfolio state
  const [portProblem, setPortProblem] = useState('');
  const [portSolution, setPortSolution] = useState('');
  const [portSlug, setPortSlug] = useState('');
  const [portArch, setPortArch] = useState('');
  const [portPublished, setPortPublished] = useState(false);
  const [portSaving, setPortSaving] = useState(false);
  const [copiedLink, setCopiedLink] = useState(false);

  // Settings state
  const [editName, setEditName] = useState('');
  const [editDesc, setEditDesc] = useState('');
  const [editBudget, setEditBudget] = useState('');
  const [editDeadline, setEditDeadline] = useState('');
  const [editGithub, setEditGithub] = useState('');
  const [editKicad, setEditKicad] = useState('');
  const [editFusion, setEditFusion] = useState('');
  const [editDocs, setEditDocs] = useState('');
  const [settingsSaving, setSettingsSaving] = useState(false);

  const loadAllData = async () => {
    try {
      setLoading(true);
      const [projData, tasksData, compsData, costsData, portData] = await Promise.all([
        projectsApi.get(projectId),
        tasksApi.list(projectId),
        componentsApi.list(projectId),
        componentsApi.costs(projectId),
        portfolioApi.get(projectId),
      ]);

      setProject(projData);
      setTasks(tasksData || []);
      setComponents(compsData || []);
      setCosts(costsData);
      setPortfolio(portData);

      if (portData) {
        setPortProblem(portData.problem || '');
        setPortSolution(portData.solution || '');
        setPortSlug(portData.slug || '');
        setPortArch(portData.architecture_data || '');
        setPortPublished(Boolean(portData.is_published));
      }

      if (projData) {
        setEditName(projData.name || '');
        setEditDesc(projData.description || '');
        setEditBudget(projData.budget || '');
        setEditDeadline(projData.deadline || '');
        setEditGithub(projData.github_url || '');
        setEditKicad(projData.kicad_url || '');
        setEditFusion(projData.fusion_url || '');
        setEditDocs(projData.docs_url || '');
      }
    } catch (err) {
      setError(err.message || 'Failed to load project');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, [projectId]);

  const handleToggleTaskStatus = async (task) => {
    const nextStatus = task.status === 'Completed' ? 'Pending' : 'Completed';
    try {
      const updated = await tasksApi.update(task.id, { status: nextStatus });
      setTasks(prev => prev.map(t => t.id === task.id ? updated : t));
      const refreshedProj = await projectsApi.get(projectId);
      setProject(refreshedProj);
    } catch (err) {
      alert('Failed to update task: ' + err.message);
    }
  };

  const handleAddTask = async (e) => {
    e.preventDefault();
    if (!newTaskName.trim()) return;

    try {
      setAddingTask(true);
      const newTask = await tasksApi.create(projectId, {
        name: newTaskName.trim(),
        description: newTaskDesc.trim() || null,
        status: 'Pending'
      });
      setTasks(prev => [...prev, newTask]);
      setNewTaskName('');
      setNewTaskDesc('');
      const refreshedProj = await projectsApi.get(projectId);
      setProject(refreshedProj);
    } catch (err) {
      alert('Failed to add task: ' + err.message);
    } finally {
      setAddingTask(false);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await tasksApi.delete(taskId);
      setTasks(prev => prev.filter(t => t.id !== taskId));
      const refreshedProj = await projectsApi.get(projectId);
      setProject(refreshedProj);
    } catch (err) {
      alert('Failed to delete task: ' + err.message);
    }
  };

  const handleAddComponent = async (e) => {
    e.preventDefault();
    if (!compName.trim()) return;

    try {
      const newComp = await componentsApi.create(projectId, {
        name: compName.trim(),
        category: compCategory,
        quantity: parseInt(compQty, 10) || 1,
        unit_price: parseFloat(compPrice) || 0.0,
        purchase_link: compLink.trim() || null,
        notes: compNotes.trim() || null,
      });

      setComponents(prev => [...prev, newComp]);
      const refreshedCosts = await componentsApi.costs(projectId);
      setCosts(refreshedCosts);
      const refreshedProj = await projectsApi.get(projectId);
      setProject(refreshedProj);

      setCompName('');
      setCompPrice('');
      setCompLink('');
      setCompNotes('');
      setShowAddComp(false);
    } catch (err) {
      alert('Failed to add component: ' + err.message);
    }
  };

  const handleDeleteComponent = async (compId) => {
    try {
      await componentsApi.delete(compId);
      setComponents(prev => prev.filter(c => c.id !== compId));
      const refreshedCosts = await componentsApi.costs(projectId);
      setCosts(refreshedCosts);
      const refreshedProj = await projectsApi.get(projectId);
      setProject(refreshedProj);
    } catch (err) {
      alert('Failed to delete component: ' + err.message);
    }
  };

  const handleEditComponent = (comp) => {
    setEditingCompId(comp.id);
    setEditCompName(comp.name);
    setEditCompCategory(comp.category || 'General');
    setEditCompQty(comp.quantity);
    setEditCompPrice(String(comp.unit_price));
    setEditCompLink(comp.purchase_link || '');
    setEditCompNotes(comp.notes || '');
  };

  const handleCancelEdit = () => {
    setEditingCompId(null);
  };

  const handleSaveEdit = async (e) => {
    e.preventDefault();
    if (!editCompName.trim()) return;
    try {
      const updated = await componentsApi.update(editingCompId, {
        name: editCompName.trim(),
        category: editCompCategory,
        quantity: parseInt(editCompQty, 10) || 1,
        unit_price: parseFloat(editCompPrice) || 0.0,
        purchase_link: editCompLink.trim() || null,
        notes: editCompNotes.trim() || null,
      });
      setComponents(prev => prev.map(c => c.id === editingCompId ? updated : c));
      const refreshedCosts = await componentsApi.costs(projectId);
      setCosts(refreshedCosts);
      const refreshedProj = await projectsApi.get(projectId);
      setProject(refreshedProj);
      setEditingCompId(null);
    } catch (err) {
      alert('Failed to update component: ' + err.message);
    }
  };

  const exportBOMToCSV = () => {
    if (components.length === 0) {
      alert('No components to export');
      return;
    }

    const headers = ['Category', 'Component', 'Quantity', 'Unit Price (INR)', 'Total Price (INR)', 'Link', 'Notes'];
    const rows = components.map(c => [
      `"${c.category || ''}"`,
      `"${c.name || ''}"`,
      c.quantity,
      `₹${c.unit_price.toFixed(2)}`,
      `₹${c.total_price.toFixed(2)}`,
      `"${c.purchase_link || ''}"`,
      `"${c.notes || ''}"`
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `BOM_${project.name.replace(/[^a-zA-Z0-9]/g, '_')}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleSavePortfolio = async (e) => {
    e.preventDefault();
    try {
      setPortSaving(true);
      const updated = await portfolioApi.update(projectId, {
        slug: portSlug.trim().toLowerCase(),
        problem: portProblem.trim(),
        solution: portSolution.trim(),
        architecture_data: portArch.trim(),
        is_published: portPublished,
      });
      setPortfolio(updated);
      alert('Portfolio details saved successfully!');
    } catch (err) {
      alert('Failed to save portfolio: ' + err.message);
    } finally {
      setPortSaving(false);
    }
  };

  const copyPublicUrl = () => {
    const url = `${window.location.origin}/p/${portSlug}`;
    navigator.clipboard.writeText(url);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2500);
  };

  const handleSaveSettings = async (e) => {
    e.preventDefault();
    try {
      setSettingsSaving(true);
      const updated = await projectsApi.update(projectId, {
        name: editName.trim(),
        description: editDesc.trim(),
        budget: editBudget ? parseFloat(editBudget) : 0.0,
        deadline: editDeadline || null,
        github_url: editGithub.trim() || null,
        kicad_url: editKicad.trim() || null,
        fusion_url: editFusion.trim() || null,
        docs_url: editDocs.trim() || null,
      });
      setProject(updated);
      alert('Project settings saved successfully!');
    } catch (err) {
      alert('Failed to update project: ' + err.message);
    } finally {
      setSettingsSaving(false);
    }
  };

  const handleDeleteProject = async () => {
    if (window.confirm(`Are you sure you want to delete "${project.name}"? This will permanently delete all tasks, hardware components, and portfolio showcase.`)) {
      try {
        await projectsApi.delete(projectId);
        navigate('/dashboard');
      } catch (err) {
        alert('Failed to delete project: ' + err.message);
      }
    }
  };

  if (loading) {
    return (
      <div className="app-container" style={{ padding: '6rem 1.5rem', textAlign: 'center', color: 'var(--text-muted)' }}>
        Loading project workspace...
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="app-container" style={{ padding: '6rem 1.5rem', textAlign: 'center' }}>
        <h2 style={{ color: 'var(--status-danger-text)', marginBottom: '0.75rem' }}>Project Not Found</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>{error || 'The requested project could not be found.'}</p>
        <Link to="/dashboard" className="btn btn-secondary">Back to Projects</Link>
      </div>
    );
  }

  const upcomingTasks = tasks.filter(t => t.status !== 'Completed').slice(0, 4);

  return (
    <div className="app-container" style={{ padding: '2rem 1.5rem 6rem' }}>
      {/* ─── Top: Back to Projects ─── */}
      <Link 
        to="/dashboard" 
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.4rem',
          fontSize: '0.85rem',
          fontWeight: 600,
          color: 'var(--text-muted)',
          marginBottom: '1.25rem',
          transition: 'color var(--transition-fast)'
        }}
      >
        <ArrowLeft size={16} />
        <span>Back to Projects</span>
      </Link>

      {/* ─── Top Workspace Header (Exact layout requested) ─── */}
      <div className="panel" style={{ marginBottom: '1.75rem', padding: '1.75rem', background: 'var(--bg-card)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem' }}>
          <div style={{ flex: 1, minWidth: '280px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap', marginBottom: '0.4rem' }}>
              <h1 style={{ fontSize: 'clamp(1.75rem, 3.5vw, 2.25rem)', fontWeight: 800, color: 'var(--text-heading)', letterSpacing: '-0.025em' }}>
                {project.name}
              </h1>
              <Badge status={project.progress === 100 ? 'Completed' : (project.status || 'In Progress')} />
            </div>

            <p style={{ color: 'var(--text-secondary)', fontSize: '0.925rem', maxWidth: '800px', lineHeight: 1.6 }}>
              {project.description || 'No description provided yet.'}
            </p>
          </div>

          {/* Quick Action: Live Portfolio / Publish */}
          <div style={{ display: 'flex', gap: '0.6rem' }}>
            {portfolio && portfolio.is_published ? (
              <Link
                to={`/p/${portfolio.slug}`}
                target="_blank"
                rel="noreferrer"
                className="btn btn-secondary btn-sm"
                style={{ gap: '0.4rem', color: 'var(--accent-blue)' }}
              >
                <Share2 size={13} />
                <span>Public Portfolio</span>
                <ExternalLink size={12} />
              </Link>
            ) : (
              <button
                onClick={() => setActiveTab('portfolio')}
                className="btn btn-primary btn-sm"
              >
                <span>Publish Portfolio</span>
              </button>
            )}
          </div>
        </div>

        {/* ─── Progress Bar with Percentage ─── */}
        <div style={{ marginTop: '1.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem', fontSize: '0.825rem' }}>
            <span style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>Project Progress</span>
            <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--accent-primary)' }}>
              {project.progress}% Completed
            </span>
          </div>
          <ProgressBar progress={project.progress} height={8} />
        </div>
      </div>

      {/* ─── Six Defined Workspace Navigation Tabs ─── */}
      <div className="workspace-tabs">
        <button
          onClick={() => setActiveTab('overview')}
          className={`workspace-tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
        >
          <Activity size={16} />
          <span>Overview</span>
        </button>

        <button
          onClick={() => setActiveTab('tasks')}
          className={`workspace-tab-btn ${activeTab === 'tasks' ? 'active' : ''}`}
        >
          <ListTodo size={16} />
          <span>Tasks</span>
          <span style={{
            fontSize: '0.72rem',
            padding: '0.1rem 0.45rem',
            borderRadius: 'var(--radius-full)',
            background: 'var(--bg-subtle)',
            color: 'var(--text-secondary)'
          }}>
            {tasks.length}
          </span>
        </button>

        <button
          onClick={() => setActiveTab('hardware')}
          className={`workspace-tab-btn ${activeTab === 'hardware' ? 'active' : ''}`}
        >
          <Cpu size={16} />
          <span>Hardware</span>
          <span style={{
            fontSize: '0.72rem',
            padding: '0.1rem 0.45rem',
            borderRadius: 'var(--radius-full)',
            background: 'var(--bg-subtle)',
            color: 'var(--text-secondary)'
          }}>
            ₹{costs ? costs.total_spent.toFixed(0) : '0'}
          </span>
        </button>

        <button
          onClick={() => setActiveTab('files')}
          className={`workspace-tab-btn ${activeTab === 'files' ? 'active' : ''}`}
        >
          <FolderGit2 size={16} />
          <span>Files & CAD</span>
        </button>

        <button
          onClick={() => setActiveTab('portfolio')}
          className={`workspace-tab-btn ${activeTab === 'portfolio' ? 'active' : ''}`}
        >
          <Share2 size={16} />
          <span>Portfolio</span>
          {portfolio && portfolio.is_published && (
            <span style={{ width: 7, height: 7, borderRadius: '50%', background: 'var(--accent-emerald)' }} />
          )}
        </button>

        <button
          onClick={() => setActiveTab('settings')}
          className={`workspace-tab-btn ${activeTab === 'settings' ? 'active' : ''}`}
        >
          <Settings size={16} />
          <span>Settings</span>
        </button>
      </div>

      {/* ─── TAB 1: OVERVIEW SECTION ─── */}
      {activeTab === 'overview' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
          {/* Key Metric Overview Cards */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '1rem'
          }}>
            <div className="metric-card">
              <div className="metric-label">Milestones Done</div>
              <div className="metric-value" style={{ color: 'var(--accent-emerald)' }}>
                {tasks.filter(t => t.status === 'Completed').length} / {tasks.length}
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-label">BOM Expenditure</div>
              <div className="metric-value" style={{ color: costs?.is_over_budget ? 'var(--status-danger-text)' : 'var(--text-heading)' }}>
                ₹{costs ? costs.total_spent.toFixed(0) : '0'}
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Remaining Budget</div>
              <div className="metric-value">
                ₹{costs ? costs.remaining_budget.toFixed(0) : '0'}
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Target Completion</div>
              <div className="metric-value" style={{ fontSize: '1.25rem' }}>
                {project.deadline || 'Ongoing'}
              </div>
            </div>
          </div>

          {/* Project Journey Visual Timeline */}
          <ProjectJourney 
            progress={project.progress} 
            isPublished={portfolio?.is_published} 
          />

          {/* Project DNA System Topology */}
          <ProjectDNA 
            technologies={project.technologies} 
            category={project.category || 'Embedded'} 
          />

          {/* Dual Column: Next Upcoming Tasks & Hardware Snapshot */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
            gap: '1.5rem'
          }}>
            {/* Next Upcoming Tasks */}
            <div className="panel">
              <div className="panel-header">
                <span className="panel-title">Immediate Milestones to Tackle</span>
                <button 
                  onClick={() => setActiveTab('tasks')}
                  className="btn btn-secondary btn-sm"
                  style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem' }}
                >
                  View All ({tasks.length})
                </button>
              </div>

              {upcomingTasks.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '2rem 1rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                  {tasks.length === 0 
                    ? 'No tasks created yet. Switch to the Tasks tab to add milestones.' 
                    : '🎉 All milestones are marked as completed! Ready to publish.'}
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {upcomingTasks.map(task => (
                    <div 
                      key={task.id}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        padding: '0.65rem 0.85rem',
                        background: 'var(--bg-subtle)',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: '0.875rem'
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                        <button
                          type="button"
                          onClick={() => handleToggleTaskStatus(task)}
                          style={{ color: 'var(--text-muted)', display: 'flex' }}
                        >
                          <Circle size={17} />
                        </button>
                        <span style={{ fontWeight: 600, color: 'var(--text-heading)' }}>
                          {task.name}
                        </span>
                      </div>
                      <Badge status="Pending" />
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Technical Resources & Artifacts */}
            <div className="panel">
              <div className="panel-header">
                <span className="panel-title">Engineering Artifacts & Links</span>
                <button 
                  onClick={() => setActiveTab('files')}
                  className="btn btn-secondary btn-sm"
                  style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem' }}
                >
                  Manage Files
                </button>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '0.65rem 0.85rem',
                  background: 'var(--bg-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.85rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Code size={15} color="var(--accent-blue)" />
                    <span style={{ fontWeight: 600 }}>Source Code (GitHub)</span>
                  </div>
                  {project.github_url ? (
                    <a href={project.github_url} target="_blank" rel="noreferrer" style={{ color: 'var(--accent-blue)', display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}>
                      <span>Open</span>
                      <ExternalLink size={12} />
                    </a>
                  ) : (
                    <span style={{ color: 'var(--text-muted)' }}>Unset</span>
                  )}
                </div>

                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '0.65rem 0.85rem',
                  background: 'var(--bg-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.85rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Cpu size={15} color="var(--accent-primary)" />
                    <span style={{ fontWeight: 600 }}>KiCad Schematics</span>
                  </div>
                  {project.kicad_url ? (
                    <a href={project.kicad_url} target="_blank" rel="noreferrer" style={{ color: 'var(--accent-primary)', display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}>
                      <span>Open</span>
                      <ExternalLink size={12} />
                    </a>
                  ) : (
                    <span style={{ color: 'var(--text-muted)' }}>Unset</span>
                  )}
                </div>

                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '0.65rem 0.85rem',
                  background: 'var(--bg-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.85rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Compass size={15} color="var(--accent-blue)" />
                    <span style={{ fontWeight: 600 }}>CAD 3D Models</span>
                  </div>
                  {project.fusion_url ? (
                    <a href={project.fusion_url} target="_blank" rel="noreferrer" style={{ color: 'var(--accent-blue)', display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}>
                      <span>Open</span>
                      <ExternalLink size={12} />
                    </a>
                  ) : (
                    <span style={{ color: 'var(--text-muted)' }}>Unset</span>
                  )}
                </div>

                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '0.65rem 0.85rem',
                  background: 'var(--bg-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.85rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <FileText size={15} color="var(--text-muted)" />
                    <span style={{ fontWeight: 600 }}>Spec Documentation</span>
                  </div>
                  {project.docs_url ? (
                    <a href={project.docs_url} target="_blank" rel="noreferrer" style={{ color: 'var(--text-secondary)', display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}>
                      <span>Open</span>
                      <ExternalLink size={12} />
                    </a>
                  ) : (
                    <span style={{ color: 'var(--text-muted)' }}>Unset</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB 2: TASKS ─── */}
      {activeTab === 'tasks' && (
        <div>
          {/* Quick Add Task Form */}
          <form onSubmit={handleAddTask} className="panel" style={{ marginBottom: '1.5rem', padding: '1rem 1.25rem' }}>
            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
              <input
                type="text"
                className="input-field"
                placeholder="Add a new milestone or engineering task..."
                value={newTaskName}
                onChange={(e) => setNewTaskName(e.target.value)}
                style={{ flex: 1 }}
              />
              <button
                type="submit"
                className="btn btn-primary"
                disabled={addingTask || !newTaskName.trim()}
              >
                <Plus size={15} />
                <span>Add Task</span>
              </button>
            </div>
          </form>

          {/* Tasks List */}
          {tasks.length === 0 ? (
            <div className="panel" style={{ textAlign: 'center', padding: '3.5rem 1.5rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
              No tasks yet. Add your first milestone above to start tracking your build progress.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
              {tasks.map((task) => {
                const isDone = task.status === 'Completed';

                return (
                  <div
                    key={task.id}
                    className="panel"
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '0.85rem 1.25rem',
                      background: isDone ? 'var(--bg-subtle)' : 'var(--bg-panel)'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                      <button
                        type="button"
                        onClick={() => handleToggleTaskStatus(task)}
                        style={{ color: isDone ? 'var(--accent-emerald)' : 'var(--text-muted)', display: 'flex', alignItems: 'center' }}
                        title={isDone ? 'Mark as Pending' : 'Mark as Completed'}
                      >
                        {isDone ? <CheckCircle2 size={20} /> : <Circle size={20} />}
                      </button>

                      <div>
                        <div style={{
                          fontSize: '0.925rem',
                          fontWeight: 600,
                          color: isDone ? 'var(--text-muted)' : 'var(--text-heading)',
                          textDecoration: isDone ? 'line-through' : 'none'
                        }}>
                          {task.name}
                        </div>
                        {task.description && (
                          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.15rem' }}>
                            {task.description}
                          </div>
                        )}
                      </div>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <Badge status={task.status} />
                      <button
                        type="button"
                        onClick={() => handleDeleteTask(task.id)}
                        className="btn btn-secondary btn-sm"
                        style={{ padding: '0.3rem 0.5rem', color: 'var(--text-muted)' }}
                        title="Delete task"
                      >
                        <Trash2 size={13} />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* ─── TAB 3: HARDWARE (BOM & COSTS) ─── */}
      {activeTab === 'hardware' && (
        <div>
          {/* Budget Alert Banners */}
          {costs && (
            <div style={{ marginBottom: '1.5rem' }}>
              {costs.is_over_budget && (
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem',
                  padding: '0.9rem 1.25rem',
                  borderRadius: 'var(--radius-sm)',
                  background: 'var(--status-danger-bg)',
                  border: '1px solid var(--status-danger-border)',
                  color: 'var(--status-danger-text)',
                  fontSize: '0.875rem',
                  marginBottom: '1rem'
                }}>
                  <AlertTriangle size={18} />
                  <span>
                    <strong>Over Budget:</strong> Total component spending exceeds your allocated budget by ₹{costs.over_budget_amount.toFixed(2)}.
                  </span>
                </div>
              )}

              {costs.is_warning && !costs.is_over_budget && (
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem',
                  padding: '0.9rem 1.25rem',
                  borderRadius: 'var(--radius-sm)',
                  background: 'var(--status-pending-bg)',
                  border: '1px solid var(--status-pending-border)',
                  color: 'var(--status-pending-text)',
                  fontSize: '0.875rem',
                  marginBottom: '1rem'
                }}>
                  <AlertTriangle size={18} />
                  <span>
                    <strong>Budget Warning:</strong> You have consumed {costs.budget_used_percentage}% of your ₹{costs.budget.toFixed(2)} budget.
                  </span>
                </div>
              )}

              {/* Financial metric summary cards */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1rem'
              }}>
                <div className="metric-card">
                  <div className="metric-label">Allocated Budget</div>
                  <div className="metric-value">₹{costs.budget.toFixed(2)}</div>
                </div>

                <div className="metric-card">
                  <div className="metric-label">Total Spent</div>
                  <div className="metric-value" style={{ color: costs.is_over_budget ? 'var(--status-danger-text)' : 'var(--text-heading)' }}>
                    ₹{costs.total_spent.toFixed(2)}
                  </div>
                </div>

                <div className="metric-card">
                  <div className="metric-label">Remaining Balance</div>
                  <div className="metric-value" style={{ color: costs.remaining_budget < 0 ? 'var(--status-danger-text)' : 'var(--accent-emerald)' }}>
                    ₹{costs.remaining_budget.toFixed(2)}
                  </div>
                </div>

                <div className="metric-card">
                  <div className="metric-label">Budget Used</div>
                  <div className="metric-value">
                    {costs.budget_used_percentage}%
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Action Row */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-heading)' }}>
              Bill of Materials ({components.length} components)
            </h2>

            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                type="button"
                onClick={exportBOMToCSV}
                className="btn btn-secondary btn-sm"
              >
                <Download size={14} />
                <span>Export CSV</span>
              </button>

              <button
                type="button"
                onClick={() => setShowAddComp(!showAddComp)}
                className="btn btn-primary btn-sm"
              >
                <Plus size={14} />
                <span>Add Component</span>
              </button>
            </div>
          </div>

          {/* Add Component Panel */}
          {showAddComp && (
            <form onSubmit={handleAddComponent} className="panel" style={{ marginBottom: '1.5rem', padding: '1.5rem' }}>
              <div className="panel-header">
                <span className="panel-title">Add Hardware Component</span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.85rem', marginBottom: '0.85rem' }}>
                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Component Name *</label>
                  <input
                    type="text"
                    className="input-field"
                    placeholder="e.g. ESP32-WROOM-32"
                    value={compName}
                    onChange={(e) => setCompName(e.target.value)}
                    required
                  />
                </div>

                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Category</label>
                  <select
                    className="input-field"
                    value={compCategory}
                    onChange={(e) => setCompCategory(e.target.value)}
                  >
                    <option value="MCU">Microcontroller / Embedded</option>
                    <option value="Sensor">Sensor</option>
                    <option value="Actuator">Actuator / Motor</option>
                    <option value="Power">Power & Battery</option>
                    <option value="PCB">PCB & Passives</option>
                    <option value="Mechanical">Mechanical / 3D Print</option>
                    <option value="General">Other / General</option>
                  </select>
                </div>

                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Quantity *</label>
                  <input
                    type="number"
                    min="1"
                    className="input-field"
                    value={compQty}
                    onChange={(e) => setCompQty(e.target.value)}
                    required
                  />
                </div>

                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Unit Price (₹ INR) *</label>
                  <input
                    type="number"
                    step="any"
                    min="0"
                    className="input-field"
                    placeholder="₹ 0.00"
                    value={compPrice}
                    onChange={(e) => setCompPrice(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.85rem', marginBottom: '1.25rem' }}>
                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Purchase / Datasheet URL</label>
                  <input
                    type="url"
                    className="input-field"
                    placeholder="https://..."
                    value={compLink}
                    onChange={(e) => setCompLink(e.target.value)}
                  />
                </div>

                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Notes / Package</label>
                  <input
                    type="text"
                    className="input-field"
                    placeholder="e.g. SMD 0805, 3.3V logic"
                    value={compNotes}
                    onChange={(e) => setCompNotes(e.target.value)}
                  />
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.6rem' }}>
                <button
                  type="button"
                  onClick={() => setShowAddComp(false)}
                  className="btn btn-secondary btn-sm"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary btn-sm"
                >
                  Save Component
                </button>
              </div>
            </form>
          )}

          {/* Edit Component Form */}
          {editingCompId && (
            <form onSubmit={handleSaveEdit} className="panel" style={{ marginBottom: '1.5rem', padding: '1.5rem' }}>
              <div className="panel-header">
                <span className="panel-title">Edit Component</span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.85rem', marginBottom: '0.85rem' }}>
                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Component Name *</label>
                  <input
                    type="text"
                    className="input-field"
                    value={editCompName}
                    onChange={(e) => setEditCompName(e.target.value)}
                    required
                  />
                </div>

                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Category</label>
                  <select
                    className="input-field"
                    value={editCompCategory}
                    onChange={(e) => setEditCompCategory(e.target.value)}
                  >
                    <option value="MCU">Microcontroller / Embedded</option>
                    <option value="Sensor">Sensor</option>
                    <option value="Actuator">Actuator / Motor</option>
                    <option value="Power">Power & Battery</option>
                    <option value="PCB">PCB & Passives</option>
                    <option value="Mechanical">Mechanical / 3D Print</option>
                    <option value="General">Other / General</option>
                  </select>
                </div>

                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Quantity *</label>
                  <input
                    type="number"
                    min="1"
                    className="input-field"
                    value={editCompQty}
                    onChange={(e) => setEditCompQty(e.target.value)}
                    required
                  />
                </div>

                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Unit Price (₹ INR) *</label>
                  <input
                    type="number"
                    step="any"
                    min="0"
                    className="input-field"
                    value={editCompPrice}
                    onChange={(e) => setEditCompPrice(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.85rem', marginBottom: '1.25rem' }}>
                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Purchase / Datasheet URL</label>
                  <input
                    type="url"
                    className="input-field"
                    placeholder="https://..."
                    value={editCompLink}
                    onChange={(e) => setEditCompLink(e.target.value)}
                  />
                </div>

                <div className="input-group" style={{ marginBottom: 0 }}>
                  <label className="input-label">Notes / Package</label>
                  <input
                    type="text"
                    className="input-field"
                    value={editCompNotes}
                    onChange={(e) => setEditCompNotes(e.target.value)}
                  />
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.6rem' }}>
                <button
                  type="button"
                  onClick={handleCancelEdit}
                  className="btn btn-secondary btn-sm"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary btn-sm"
                >
                  Save Changes
                </button>
              </div>
            </form>
          )}

          {/* Component BOM Table */}
          {components.length === 0 ? (
            <div className="panel" style={{ textAlign: 'center', padding: '3.5rem 1.5rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
              No hardware components logged yet. Click "Add Component" above to build your Bill of Materials.
            </div>
          ) : (
            <div className="panel" style={{ overflowX: 'auto', padding: 0 }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem', textAlign: 'left' }}>
                <thead>
                  <tr style={{
                    borderBottom: '1px solid var(--border-default)',
                    background: 'var(--bg-subtle)',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    color: 'var(--text-muted)',
                    textTransform: 'uppercase'
                  }}>
                    <th style={{ padding: '0.85rem 1.25rem' }}>Component</th>
                    <th style={{ padding: '0.85rem 1.25rem' }}>Category</th>
                    <th style={{ padding: '0.85rem 1.25rem' }}>Qty</th>
                    <th style={{ padding: '0.85rem 1.25rem' }}>Unit Price</th>
                    <th style={{ padding: '0.85rem 1.25rem' }}>Total</th>
                    <th style={{ padding: '0.85rem 1.25rem' }}>Link</th>
                    <th style={{ padding: '0.85rem 1.25rem', textAlign: 'right' }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {components.map((c) => (
                    <tr key={c.id} style={{ borderBottom: '1px solid var(--border-default)' }}>
                      <td style={{ padding: '0.85rem 1.25rem', fontWeight: 600, color: 'var(--text-heading)' }}>
                        {c.name}
                        {c.notes && (
                          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 400, marginTop: '0.15rem' }}>
                            {c.notes}
                          </div>
                        )}
                      </td>
                      <td style={{ padding: '0.85rem 1.25rem' }}>
                        <span className="tech-tag">{c.category}</span>
                      </td>
                      <td style={{ padding: '0.85rem 1.25rem', fontFamily: 'var(--font-mono)' }}>{c.quantity}</td>
                      <td style={{ padding: '0.85rem 1.25rem', fontFamily: 'var(--font-mono)' }}>₹{c.unit_price.toFixed(2)}</td>
                      <td style={{ padding: '0.85rem 1.25rem', fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--text-heading)' }}>
                        ₹{c.total_price.toFixed(2)}
                      </td>
                      <td style={{ padding: '0.85rem 1.25rem' }}>
                        {c.purchase_link ? (
                          <a href={c.purchase_link} target="_blank" rel="noreferrer" style={{ color: 'var(--accent-blue)', display: 'inline-flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.8rem' }}>
                            <span>View</span>
                            <ExternalLink size={12} />
                          </a>
                        ) : (
                          <span style={{ color: 'var(--text-muted)' }}>—</span>
                        )}
                      </td>
                      <td style={{ padding: '0.85rem 1.25rem', textAlign: 'right' }}>
                        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.35rem' }}>
                          <button
                            type="button"
                            onClick={() => handleEditComponent(c)}
                            className="btn btn-secondary btn-sm"
                            style={{ padding: '0.3rem 0.5rem', color: 'var(--accent-blue)' }}
                            title="Edit component"
                          >
                            <Edit2 size={13} />
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDeleteComponent(c.id)}
                            className="btn btn-secondary btn-sm"
                            style={{ padding: '0.3rem 0.5rem', color: 'var(--text-muted)' }}
                            title="Delete component"
                          >
                            <Trash2 size={13} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* ─── TAB 4: FILES & CAD ARTIFACTS ─── */}
      {activeTab === 'files' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="panel" style={{ padding: '1.5rem' }}>
            <div className="panel-header">
              <span className="panel-title">Technical Design Files & Schematics</span>
              <button 
                onClick={() => setActiveTab('settings')}
                className="btn btn-secondary btn-sm"
                style={{ gap: '0.35rem' }}
              >
                <Settings size={13} />
                <span>Configure URLs</span>
              </button>
            </div>

            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.6 }}>
              Centralize your Git repositories, CAD modeling files, and PCB design assets for this build.
            </p>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '1.25rem'
            }}>
              {/* GitHub */}
              <div className="panel" style={{ background: 'var(--bg-subtle)', padding: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.75rem' }}>
                  <Code size={18} color="var(--accent-blue)" />
                  <h4 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-heading)' }}>
                    GitHub Repository
                  </h4>
                </div>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                  Firmware, drivers, API backend, and frontend repository code.
                </p>
                {project.github_url ? (
                  <a href={project.github_url} target="_blank" rel="noreferrer" className="btn btn-secondary btn-sm" style={{ width: '100%', gap: '0.4rem' }}>
                    <span>Open GitHub Repo</span>
                    <ExternalLink size={12} />
                  </a>
                ) : (
                  <button onClick={() => setActiveTab('settings')} className="btn btn-secondary btn-sm" style={{ width: '100%', color: 'var(--text-muted)' }}>
                    + Add GitHub Link
                  </button>
                )}
              </div>

              {/* KiCad */}
              <div className="panel" style={{ background: 'var(--bg-subtle)', padding: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.75rem' }}>
                  <Cpu size={18} color="var(--accent-primary)" />
                  <h4 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-heading)' }}>
                    KiCad PCB & Schematics
                  </h4>
                </div>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                  Schematic diagrams, netlists, and Gerber fabrication files.
                </p>
                {project.kicad_url ? (
                  <a href={project.kicad_url} target="_blank" rel="noreferrer" className="btn btn-secondary btn-sm" style={{ width: '100%', gap: '0.4rem' }}>
                    <span>Open KiCad Schematics</span>
                    <ExternalLink size={12} />
                  </a>
                ) : (
                  <button onClick={() => setActiveTab('settings')} className="btn btn-secondary btn-sm" style={{ width: '100%', color: 'var(--text-muted)' }}>
                    + Add KiCad Link
                  </button>
                )}
              </div>

              {/* CAD 3D Models */}
              <div className="panel" style={{ background: 'var(--bg-subtle)', padding: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.75rem' }}>
                  <Compass size={18} color="var(--accent-blue)" />
                  <h4 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-heading)' }}>
                    Fusion 360 / CAD
                  </h4>
                </div>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                  3D enclosure models, STEP exports, and mechanical assemblies.
                </p>
                {project.fusion_url ? (
                  <a href={project.fusion_url} target="_blank" rel="noreferrer" className="btn btn-secondary btn-sm" style={{ width: '100%', gap: '0.4rem' }}>
                    <span>Open CAD Model</span>
                    <ExternalLink size={12} />
                  </a>
                ) : (
                  <button onClick={() => setActiveTab('settings')} className="btn btn-secondary btn-sm" style={{ width: '100%', color: 'var(--text-muted)' }}>
                    + Add CAD Model Link
                  </button>
                )}
              </div>

              {/* Documentation */}
              <div className="panel" style={{ background: 'var(--bg-subtle)', padding: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.75rem' }}>
                  <FileText size={18} color="var(--text-muted)" />
                  <h4 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-heading)' }}>
                    Technical Documentation
                  </h4>
                </div>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                  Datasheets, component manuals, and lab test reports.
                </p>
                {project.docs_url ? (
                  <a href={project.docs_url} target="_blank" rel="noreferrer" className="btn btn-secondary btn-sm" style={{ width: '100%', gap: '0.4rem' }}>
                    <span>Open Documentation</span>
                    <ExternalLink size={12} />
                  </a>
                ) : (
                  <button onClick={() => setActiveTab('settings')} className="btn btn-secondary btn-sm" style={{ width: '100%', color: 'var(--text-muted)' }}>
                    + Add Docs Link
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB 5: PORTFOLIO SHOWCASE BUILDER ─── */}
      {activeTab === 'portfolio' && (
        <form onSubmit={handleSavePortfolio}>
          <div className="panel" style={{ marginBottom: '1.5rem', padding: '1.75rem' }}>
            <div className="panel-header">
              <span className="panel-title">Public Portfolio Showcase</span>

              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ fontSize: '0.825rem', fontWeight: 600, color: portPublished ? 'var(--accent-emerald)' : 'var(--text-muted)' }}>
                  {portPublished ? '● Published' : '○ Draft'}
                </span>
                <button
                  type="button"
                  onClick={() => setPortPublished(!portPublished)}
                  className={`btn ${portPublished ? 'btn-secondary' : 'btn-primary'} btn-sm`}
                >
                  {portPublished ? 'Switch to Draft' : 'Publish Portfolio'}
                </button>
              </div>
            </div>

            {/* Public Link Share Bar */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '0.85rem 1.25rem',
              background: 'var(--bg-subtle)',
              border: '1px solid var(--border-default)',
              borderRadius: 'var(--radius-sm)',
              marginBottom: '1.5rem',
              flexWrap: 'wrap',
              gap: '0.75rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Public link:</span>
                <code style={{ color: 'var(--text-heading)', fontWeight: 600, background: 'var(--bg-canvas)', padding: '0.2rem 0.5rem', borderRadius: 'var(--radius-xs)' }}>
                  /p/{portSlug || 'your-slug'}
                </code>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  type="button"
                  onClick={copyPublicUrl}
                  className="btn btn-secondary btn-sm"
                  disabled={!portSlug}
                >
                  {copiedLink ? <Check size={13} color="var(--accent-emerald)" /> : <Copy size={13} />}
                  <span>{copiedLink ? 'Copied!' : 'Copy Link'}</span>
                </button>

                {portSlug && (
                  <Link
                    to={`/p/${portSlug}`}
                    target="_blank"
                    className="btn btn-secondary btn-sm"
                    style={{ color: 'var(--accent-blue)' }}
                  >
                    <span>View Public Page</span>
                    <ExternalLink size={13} />
                  </Link>
                )}
              </div>
            </div>

            <div className="input-group">
              <label className="input-label">Custom URL Slug *</label>
              <input
                type="text"
                className="input-field"
                placeholder="e.g. smart-irrigation-hub"
                value={portSlug}
                onChange={(e) => setPortSlug(e.target.value.toLowerCase().replace(/[^a-z0-9-]/g, ''))}
                required
              />
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Letters, numbers, and hyphens only</span>
            </div>

            <div className="input-group">
              <label className="input-label">The Problem / Challenge</label>
              <textarea
                className="input-field"
                rows={4}
                placeholder="What real-world problem or challenge does this project solve? What constraints did you have?"
                value={portProblem}
                onChange={(e) => setPortProblem(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label className="input-label">Your Solution & Engineering Approach</label>
              <textarea
                className="input-field"
                rows={5}
                placeholder="How did you solve it? Detail your custom hardware, firmware, software architecture, and key achievements."
                value={portSolution}
                onChange={(e) => setPortSolution(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label className="input-label">System Architecture & Data Flow</label>
              <textarea
                className="input-field"
                rows={4}
                placeholder="e.g. Temperature Sensor (I2C) → ESP32 Microcontroller → FreeRTOS Task → MQTT over WiFi → FastAPI Backend → Web Dashboard"
                value={portArch}
                onChange={(e) => setPortArch(e.target.value)}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={portSaving}
              >
                <span>{portSaving ? 'Saving...' : 'Save Portfolio Details'}</span>
              </button>
            </div>
          </div>
        </form>
      )}

      {/* ─── TAB 6: SETTINGS ─── */}
      {activeTab === 'settings' && (
        <div>
          <form onSubmit={handleSaveSettings} className="panel" style={{ marginBottom: '1.5rem', padding: '1.75rem' }}>
            <div className="panel-header">
              <span className="panel-title">Project Settings</span>
            </div>

            <div className="input-group">
              <label className="input-label">Project Name *</label>
              <input
                type="text"
                className="input-field"
                value={editName}
                onChange={(e) => setEditName(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <label className="input-label">Description</label>
              <textarea
                className="input-field"
                rows={3}
                value={editDesc}
                onChange={(e) => setEditDesc(e.target.value)}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
              <div className="input-group">
                <label className="input-label">Total Budget (₹ INR)</label>
                <input
                  type="number"
                  step="any"
                  className="input-field"
                  value={editBudget}
                  onChange={(e) => setEditBudget(e.target.value)}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Target Completion Deadline</label>
                <input
                  type="date"
                  className="input-field"
                  value={editDeadline || ''}
                  onChange={(e) => setEditDeadline(e.target.value)}
                />
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
              <div className="input-group">
                <label className="input-label">GitHub Repository URL</label>
                <input
                  type="url"
                  className="input-field"
                  value={editGithub}
                  onChange={(e) => setEditGithub(e.target.value)}
                />
              </div>

              <div className="input-group">
                <label className="input-label">KiCad Schematics URL</label>
                <input
                  type="url"
                  className="input-field"
                  value={editKicad}
                  onChange={(e) => setEditKicad(e.target.value)}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Fusion 360 / CAD Model URL</label>
                <input
                  type="url"
                  className="input-field"
                  value={editFusion}
                  onChange={(e) => setEditFusion(e.target.value)}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Documentation URL</label>
                <input
                  type="url"
                  className="input-field"
                  value={editDocs}
                  onChange={(e) => setEditDocs(e.target.value)}
                />
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.25rem' }}>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={settingsSaving}
              >
                <span>{settingsSaving ? 'Saving...' : 'Save Changes'}</span>
              </button>
            </div>
          </form>

          {/* Danger Zone */}
          <div className="panel" style={{ borderColor: 'var(--status-danger-border)', padding: '1.75rem' }}>
            <div className="panel-header" style={{ borderColor: 'var(--status-danger-border)' }}>
              <span className="panel-title" style={{ color: 'var(--status-danger-text)' }}>
                Danger Zone
              </span>
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '1.25rem', lineHeight: 1.5 }}>
              Permanently delete this project. This will remove all tasks, hardware components, and your public portfolio showcase. This action cannot be undone.
            </p>
            <button
              type="button"
              onClick={handleDeleteProject}
              className="btn btn-danger"
            >
              <Trash2 size={14} />
              <span>Delete Project</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
