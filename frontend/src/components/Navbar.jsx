import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { Plus, LogOut, Sun, Moon, LayoutDashboard } from 'lucide-react';

export default function Navbar() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="app-container navbar-inner">
        {/* Brand */}
        <Link to={user ? "/dashboard" : "/"} className="nav-brand">
          <span className="brand-dot" />
          <span>ProjectPulse</span>
          <span style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.7rem',
            fontWeight: 500,
            color: 'var(--text-muted)',
            marginLeft: '-0.15rem'
          }}>
            v2
          </span>
        </Link>

        {/* Links */}
        <div className="nav-links">
          {/* Theme toggle */}
          <button
            onClick={toggleTheme}
            className="theme-toggle"
            title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
          >
            {theme === 'dark' ? <Sun size={15} /> : <Moon size={15} />}
          </button>

          {user ? (
            <>
              <Link
                to="/dashboard"
                className={`nav-item ${location.pathname === '/dashboard' ? 'active' : ''}`}
                style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}
              >
                <LayoutDashboard size={15} />
                <span>Dashboard</span>
              </Link>

              <Link
                to="/create"
                className="btn btn-primary btn-sm"
                style={{ gap: '0.3rem' }}
              >
                <Plus size={14} />
                <span>New Project</span>
              </Link>

              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.65rem',
                borderLeft: '1px solid var(--border-default)',
                paddingLeft: '0.85rem'
              }}>
                <span style={{
                  fontSize: '0.8rem',
                  color: 'var(--text-secondary)',
                  fontWeight: 500
                }}>
                  <strong style={{ color: 'var(--text-heading)' }}>{user.username}</strong>
                </span>

                <button
                  onClick={handleLogout}
                  className="btn btn-secondary btn-sm"
                  title="Sign out"
                  style={{ padding: '0.3rem 0.5rem' }}
                >
                  <LogOut size={14} />
                </button>
              </div>
            </>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Link to="/login" className="nav-item">Sign In</Link>
              <Link to="/signup" className="btn btn-primary btn-sm">Get Started</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
