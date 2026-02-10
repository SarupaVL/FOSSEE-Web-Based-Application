import React from 'react';

const StatCard = ({ title, value, unit, color }) => {
    return (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', fontWeight: 500 }}>{title}</span>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.25rem' }}>
                <span style={{ fontSize: '1.5rem', fontWeight: 700, color: color || 'var(--text-main)' }}>{value}</span>
                {unit && <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>{unit}</span>}
            </div>
        </div>
    );
};

export default StatCard;
