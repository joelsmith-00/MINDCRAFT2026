import React from 'react';

export default function Footer() {
    return (
        <footer style={{
            borderTop: '1px solid var(--glass-border)',
            marginTop: '60px',
            padding: '60px 0 20px 0',
            background: 'rgba(15, 23, 42, 0.4)'
        }}>
            <div className="container">
                <div style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    justifyContent: 'space-between',
                    gap: '40px',
                    marginBottom: '40px'
                }}>
                    <div>
                        <h3 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '20px' }}>SEA<span style={{ color: 'var(--color-primary)' }}>GUARD</span></h3>
                        <p style={{ color: 'var(--color-text-muted)', maxWidth: '300px' }}>
                            Protecting lives and livelihoods with offline-first artificial intelligence.
                        </p>
                    </div>

                    <div>
                        <h4 style={{ fontWeight: 600, marginBottom: '16px' }}>System</h4>
                        <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px', color: 'var(--color-text-muted)' }}>
                            <li>Neural Border Engine</li>
                            <li>Mesh Networking</li>
                            <li>Wearable Integration</li>
                            <li>Authority Dashboard</li>
                        </ul>
                    </div>
                </div>

                <div style={{
                    borderTop: '1px solid var(--glass-border)',
                    paddingTop: '20px',
                    textAlign: 'center',
                    color: 'var(--color-text-muted)',
                    fontSize: '0.875rem'
                }}>
                    &copy; 2026 SeaGuard Maritime Safety Systems. Built for Hackathon Demo.
                </div>
            </div>
        </footer>
    );
}
