import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { AlertCircle, ArrowRight } from 'lucide-react';

export default function Login() {
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!usernameOrEmail || !password) {
      setError('Username/Email and Password are required');
      return;
    }

    setError('');
    setLoading(true);

    try {
      await login(usernameOrEmail, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fillDevDemoCredentials = () => {
    // Development-only local test credentials
    setUsernameOrEmail('makertest');
    setPassword('securepassword123');
    setError('');
  };

  return (
    <div className="app-container" style={{
      minHeight: 'calc(100vh - 100px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem 1rem'
    }}>
      <div className="panel" style={{ maxWidth: '420px', width: '100%', padding: '2.25rem' }}>
        <div style={{ marginBottom: '1.75rem', borderBottom: '1px solid var(--border-default)', paddingBottom: '1rem' }}>
          <p style={{
            fontSize: '0.8rem',
            fontWeight: 600,
            color: 'var(--accent-primary)',
            marginBottom: '0.35rem'
          }}>
            Welcome back
          </p>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-heading)' }}>
            Sign in to BuildFolio
          </h2>
        </div>

        {error && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.65rem 0.85rem',
            background: 'var(--status-danger-bg)',
            border: '1px solid var(--status-danger-border)',
            borderRadius: 'var(--radius-sm)',
            color: 'var(--status-danger-text)',
            fontSize: '0.825rem',
            marginBottom: '1.25rem'
          }}>
            <AlertCircle size={15} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label className="input-label">Username or Email</label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g. makertest"
              value={usernameOrEmail}
              onChange={(e) => setUsernameOrEmail(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label className="input-label">Password</label>
            <input
              type="password"
              className="input-field"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '0.75rem', padding: '0.65rem' }}
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
            {!loading && <ArrowRight size={15} />}
          </button>
        </form>

        {/* Development-Only Demo Credential Helper */}
        <div style={{
          marginTop: '1.5rem',
          padding: '0.75rem',
          border: '1px dashed var(--border-default)',
          borderRadius: 'var(--radius-sm)',
          background: 'var(--bg-subtle)'
        }}>
          <div style={{
            fontSize: '0.72rem',
            fontWeight: 600,
            color: 'var(--text-muted)',
            marginBottom: '0.35rem',
            textTransform: 'uppercase'
          }}>
            Dev Environment Only
          </div>
          <button
            type="button"
            onClick={fillDevDemoCredentials}
            style={{
              fontSize: '0.8rem',
              color: 'var(--accent-primary)',
              textAlign: 'left',
              cursor: 'pointer',
              textDecoration: 'underline',
              fontWeight: 500
            }}
          >
            Auto-fill test account (makertest)
          </button>
        </div>

        <div style={{
          marginTop: '1.5rem',
          paddingTop: '1rem',
          borderTop: '1px solid var(--border-default)',
          textAlign: 'center',
          fontSize: '0.85rem',
          color: 'var(--text-secondary)'
        }}>
          New here?{' '}
          <Link to="/signup" style={{ color: 'var(--text-heading)', fontWeight: 600, textDecoration: 'underline' }}>
            Create an account
          </Link>
        </div>
      </div>
    </div>
  );
}
