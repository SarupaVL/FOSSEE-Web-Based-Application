import React from 'react';
import { Bar } from 'react-chartjs-2';
import StatCard from './StatCard';

const Dashboard = ({ summary, chartData, onUpload, setFile, file }) => {
    return (
        <div className="container" style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '2rem' }}>

            {/* Upload Section */}
            <div className="card">
                <h3 style={{ marginBottom: '1rem', color: 'var(--text-main)' }}>Upload New Data</h3>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
                    <input
                        type="file"
                        accept=".csv"
                        onChange={(e) => setFile(e.target.files[0])}
                        style={{ flex: 1, minWidth: '200px' }}
                    />
                    <button
                        onClick={onUpload}
                        className="btn-primary"
                        disabled={!file}
                        style={{ opacity: file ? 1 : 0.6 }}
                    >
                        Analyze Data
                    </button>
                </div>
            </div>

            {summary && (
                <>
                    {/* Stats Grid */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
                        <StatCard title="Total Equipment" value={summary.total_equipment} color="var(--primary)" />
                        <StatCard title="Avg Flowrate" value={summary.average_flowrate.toFixed(2)} unit="m³/h" />
                        <StatCard title="Avg Pressure" value={summary.average_pressure.toFixed(2)} unit="bar" />
                        <StatCard title="Avg Temperature" value={summary.average_temperature.toFixed(2)} unit="°C" />
                    </div>

                    {/* Chart Section */}
                    <div className="card" style={{ height: '400px', display: 'flex', flexDirection: 'column' }}>
                        <h3 style={{ marginBottom: '1rem' }}>Equipment Type Distribution</h3>
                        <div style={{ flex: 1, position: 'relative', minHeight: 0 }}>
                            <Bar
                                data={chartData}
                                options={{
                                    responsive: true,
                                    maintainAspectRatio: false,
                                    plugins: {
                                        legend: {
                                            position: 'top',
                                        },
                                    },
                                }}
                            />
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default Dashboard;
