import React from 'react';

const Navbar = ({ onLogout }) => {
    return (
        <nav style={{
            background: 'var(--surface)',
            borderBottom: '1px solid var(--border)',
            padding: '1rem 2rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <h2 style={{ color: 'var(--primary)', fontSize: '1.5rem' }}>Chemical Equipment Parameter Visualizer</h2>
            </div>
            <button onClick={onLogout} className="btn-danger">
                Logout
            </button>
        </nav>
    );
};

export default Navbar;
