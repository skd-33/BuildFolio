import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { AlertCircle, ArrowRight } from 'lucide-react';

export default function Signup() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !username || !password) {
      setError('All required fields must be filled');
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setError('');
    setLoading(true);

    try {
      await register({
        email,
        username,
        display_name: displayName || username,
        password,
      });
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container" style={{
      minHeight: 'calc(100vh - 100px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem 1rem'
    }}>
      <div className="panel" style={{ maxWidth: '440px', width: '100%', padding: '2.25rem' }}>
        <div style={{ marginBottom: '1.75rem', borderBottom: '1px solid var(--border-default)', paddingBottom: '1rem' }}>
          <p style={{
            fontSize: '0.8rem',
            fontWeight: 600,
            color: 'var(--accent-primary)',
            marginBottom: '0.35rem'
          }}>
            Get started
          </p>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-heading)' }}>
            Create your account
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
            <label className="input-label">Email Address *</label>
            <input
              type="email"
              className="input-field"
              placeholder="you@university.edu"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label className="input-label">Username *</label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g. alex_builds"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label className="input-label">Full Name</label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g. Alex Chen"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label className="input-label">Password *</label>
            <input
              type="password"
              className="input-field"
              placeholder="Minimum 6 characters"
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
            {loading ? 'Creating account...' : 'Create Account'}
            {!loading && <ArrowRight size={15} />}
          </button>
        </form>

        <div style={{
          marginTop: '1.5rem',
          paddingTop: '1rem',
          borderTop: '1px solid var(--border-default)',
          textAlign: 'center',
          fontSize: '0.85rem',
          color: 'var(--text-secondary)'
        }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: 'var(--text-heading)', fontWeight: 600, textDecoration: 'underline' }}>
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
