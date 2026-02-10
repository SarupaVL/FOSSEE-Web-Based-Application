import { useEffect, useState } from "react";
import axios from "axios";

const History = ({ token }) => {
    const [history, setHistory] = useState([]);

    const fetchHistory = async () => {
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/history/`, {
                headers: {
                    Authorization: `Token ${token}`,
                },
            });
            setHistory(response.data);
        } catch (error) {
            console.error("Error fetching history:", error);
        }
    };

    const downloadReport = async (uploadId) => {
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/report/${uploadId}/`, {
                headers: {
                    Authorization: `Token ${token}`,
                },
                responseType: 'blob',
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `report_${uploadId}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error("Error downloading report:", error);
        }
    };

    useEffect(() => {
        fetchHistory();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <div className="container" style={{ marginTop: 0 }}>
            {history.length > 0 && (
                <div className="card">
                    <h3 style={{ marginBottom: '1.5rem' }}>Recent Upload History</h3>
                    <div style={{ overflowX: 'auto' }}>
                        <table>
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Total Items</th>
                                    <th>Avg Statistics</th>
                                    <th>Distribution Top</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {history.map((item) => (
                                    <tr key={item.id}>
                                        <td>
                                            <span style={{ fontWeight: 500 }}>{new Date(item.created_at).toLocaleDateString()}</span>
                                            <br />
                                            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{new Date(item.created_at).toLocaleTimeString()}</span>
                                        </td>
                                        <td>{item.total_equipment}</td>
                                        <td>
                                            <div style={{ fontSize: '0.9rem' }}>
                                                Flow: <strong>{item.average_flowrate.toFixed(1)}</strong><br />
                                                Press: <strong>{item.average_pressure.toFixed(1)}</strong><br />
                                                Temp: <strong>{item.average_temperature.toFixed(1)}</strong>
                                            </div>
                                        </td>
                                        <td>
                                            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                                                {Object.entries(item.type_distribution).slice(0, 3).map(([type, count]) => (
                                                    <span key={type} className="status-badge">{type}: {count}</span>
                                                ))}
                                                {Object.keys(item.type_distribution).length > 3 && <span style={{ fontSize: '0.8rem' }}>...</span>}
                                            </div>
                                        </td>
                                        <td>
                                            <button
                                                onClick={() => downloadReport(item.id)}
                                                className="btn-primary"
                                                style={{ background: 'var(--success)', fontSize: '0.9rem' }}
                                            >
                                                PDF Report
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
};

export default History;
