import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { projectsApi } from '../api/client';
import { 
  ArrowLeft, 
  Plus, 
  Trash2, 
  Cpu, 
  Layers, 
  Code 
} from 'lucide-react';

const TEMPLATES = {
  embedded: {
    name: 'IoT / Embedded',
    icon: Cpu,
    tech: 'ESP32, C++, FreeRTOS, MQTT, KiCad',
    tasks: [
      'Component Sourcing & BOM Finalization',
      'Schematic Design & PCB Layout',
      'Firmware & Sensor Driver Development',
      'Enclosure CAD & 3D Prototyping',
      'Integration & Testing'
    ]
  },
  robotics: {
    name: 'Robotics',
    icon: Layers,
    tech: 'ROS2, Python, SolidWorks, Arduino, BLDC',
    tasks: [
      'Kinematics & Chassis Modeling',
      'Motor Driver & Actuator Selection',
      'Power Distribution & Battery Management',
      'Control Loop & Sensor Fusion Firmware',
      'Field Testing & Calibration'
    ]
  },
  software: {
    name: 'Full-Stack',
    icon: Code,
    tech: 'Python, FastAPI, React, SQLite, PyTorch',
    tasks: [
      'Architecture & API Design',
      'Database Schema & Migrations',
      'Core Backend Logic',
      'Frontend Dashboard',
      'Testing & Deployment'
    ]
  }
};

export default function CreateProject() {
  const navigate = useNavigate();

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [technologies, setTechnologies] = useState('');
  const [deadline, setDeadline] = useState('');
  const [budget, setBudget] = useState('');

  // Links
  const [githubUrl, setGithubUrl] = useState('');
  const [kicadUrl, setKicadUrl] = useState('');
  const [fusionUrl, setFusionUrl] = useState('');
  const [docsUrl, setDocsUrl] = useState('');
  const [demoUrl, setDemoUrl] = useState('');

  // Initial Tasks
  const [tasks, setTasks] = useState(['', '', '']);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const applyTemplate = (key) => {
    const t = TEMPLATES[key];
    if (!t) return;
    if (!technologies) setTechnologies(t.tech);
    setTasks([...t.tasks]);
  };

  const handleTaskChange = (index, value) => {
    const next = [...tasks];
    next[index] = value;
    setTasks(next);
  };

  const addTaskRow = () => {
    setTasks([...tasks, '']);
  };

  const removeTaskRow = (index) => {
    setTasks(tasks.filter((_, idx) => idx !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Project name is required');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const validTasks = tasks.map(t => t.trim()).filter(Boolean);

      const payload = {
        name: name.trim(),
        description: description.trim() || null,
        technologies: technologies.trim() || null,
        deadline: deadline || null,
        budget: budget ? parseFloat(budget) : 0.0,
        github_url: githubUrl.trim() || null,
        kicad_url: kicadUrl.trim() || null,
        fusion_url: fusionUrl.trim() || null,
        docs_url: docsUrl.trim() || null,
        demo_url: demoUrl.trim() || null,
        initial_tasks: validTasks.length > 0 ? validTasks : undefined
      };

      const project = await projectsApi.create(payload);
      navigate(`/project/${project.id}`);
    } catch (err) {
      setError(err.message || 'Failed to create project');
      setLoading(false);
    }
  };

  return (
    <div className="app-container" style={{ maxWidth: '840px', padding: '2.5rem 1.5rem 6rem' }}>
      <Link to="/dashboard" style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '0.4rem',
        color: 'var(--text-muted)',
        fontSize: '0.85rem',
        fontWeight: 500,
        marginBottom: '1.5rem'
      }}>
        <ArrowLeft size={15} />
        <span>Back to Dashboard</span>
      </Link>

      <div style={{ marginBottom: '2rem', borderBottom: '1px solid var(--border-default)', paddingBottom: '1.25rem' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-heading)', letterSpacing: '-0.02em' }}>
          Create New Project
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.35rem' }}>
          Start by giving your project a name. You can add details later.
        </p>
      </div>

      {/* Templates */}
      <div className="panel" style={{ marginBottom: '1.5rem' }}>
        <div className="panel-header">
          <span className="panel-title">Quick Start Templates</span>
        </div>
        <div style={{ display: 'flex', gap: '0.65rem', flexWrap: 'wrap' }}>
          {Object.entries(TEMPLATES).map(([key, item]) => {
            const Icon = item.icon;
            return (
              <button
                key={key}
                type="button"
                onClick={() => applyTemplate(key)}
                className="btn btn-secondary btn-sm"
                style={{ gap: '0.4rem' }}
              >
                <Icon size={14} color="var(--accent-primary)" />
                <span>{item.name}</span>
              </button>
            );
          })}
        </div>
      </div>

      {error && (
        <div style={{
          padding: '0.75rem 1rem',
          background: 'var(--status-danger-bg)',
          border: '1px solid var(--status-danger-border)',
          borderRadius: 'var(--radius-sm)',
          color: 'var(--status-danger-text)',
          fontSize: '0.85rem',
          marginBottom: '1.5rem'
        }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Core Info */}
        <div className="panel" style={{ marginBottom: '1.5rem' }}>
          <div className="panel-header">
            <span className="panel-title">Project Details</span>
          </div>

          <div className="input-group">
            <label className="input-label">Project Name *</label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g. Autonomous Rover with Telemetry"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label className="input-label">Description</label>
            <textarea
              className="input-field"
              rows={3}
              placeholder="What are you building and why?"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label className="input-label">Technologies (comma separated)</label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g. ESP32, FreeRTOS, MQTT, KiCad, Python"
              value={technologies}
              onChange={(e) => setTechnologies(e.target.value)}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div className="input-group">
              <label className="input-label">Target Deadline</label>
              <input
                type="date"
                className="input-field"
                value={deadline}
                onChange={(e) => setDeadline(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label className="input-label">Budget (₹ INR)</label>
              <input
                type="number"
                step="any"
                className="input-field"
                placeholder="e.g. 5000"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* Initial Tasks */}
        <div className="panel" style={{ marginBottom: '1.5rem' }}>
          <div className="panel-header">
            <span className="panel-title">Initial Tasks</span>
            <button
              type="button"
              onClick={addTaskRow}
              className="btn btn-secondary btn-sm"
            >
              <Plus size={14} />
              <span>Add Task</span>
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {tasks.map((task, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.8rem',
                  color: 'var(--text-muted)',
                  width: '28px',
                  textAlign: 'right',
                  fontWeight: 500
                }}>
                  {idx + 1}.
                </span>
                <input
                  type="text"
                  className="input-field"
                  placeholder={`Task ${idx + 1}...`}
                  value={task}
                  onChange={(e) => handleTaskChange(idx, e.target.value)}
                  style={{ flex: 1 }}
                />
                {tasks.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeTaskRow(idx)}
                    className="btn btn-secondary btn-sm"
                    style={{ padding: '0.45rem', color: 'var(--text-muted)' }}
                    title="Remove"
                  >
                    <Trash2 size={14} />
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Links */}
        <div className="panel" style={{ marginBottom: '2rem' }}>
          <div className="panel-header">
            <span className="panel-title">Project Links</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
            <div className="input-group">
              <label className="input-label">GitHub Repository</label>
              <input
                type="url"
                className="input-field"
                placeholder="https://github.com/..."
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label className="input-label">KiCad / Schematics URL</label>
              <input
                type="url"
                className="input-field"
                placeholder="https://..."
                value={kicadUrl}
                onChange={(e) => setKicadUrl(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label className="input-label">Fusion 360 / CAD Model URL</label>
              <input
                type="url"
                className="input-field"
                placeholder="https://..."
                value={fusionUrl}
                onChange={(e) => setFusionUrl(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label className="input-label">Documentation URL</label>
              <input
                type="url"
                className="input-field"
                placeholder="https://..."
                value={docsUrl}
                onChange={(e) => setDocsUrl(e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
          <Link to="/dashboard" className="btn btn-secondary">
            Cancel
          </Link>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            <span>{loading ? 'Creating...' : 'Create Project'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
