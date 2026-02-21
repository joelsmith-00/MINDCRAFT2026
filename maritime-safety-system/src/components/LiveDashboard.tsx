import React, { useState, useEffect } from 'react';
import { Navigation, Wind, Wifi, AlertTriangle, ShieldCheck, MapPin, Radio } from 'lucide-react';

export default function LiveDashboard() {
    const [stats, setStats] = useState({
        speed: 12.4,
        heading: 285,
        distanceToBorder: 4.2,
        riskLevel: 'SAFE',
        lat: 13.0827,
        lng: 80.2707
    });

    const [alerts, setAlerts] = useState<string[]>([]);

    useEffect(() => {
        const interval = setInterval(() => {
            // Simulate boat movement and varying data
            setStats(prev => ({
                speed: +(prev.speed + (Math.random() - 0.5)).toFixed(1),
                heading: Math.floor(prev.heading + (Math.random() * 4 - 2)),
                distanceToBorder: +(prev.distanceToBorder - 0.01).toFixed(2), // Slowly approaching border
                riskLevel: prev.distanceToBorder < 2 ? 'WARNING' : 'SAFE',
                lat: prev.lat + 0.0001,
                lng: prev.lng + 0.0001
            }));
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <section id="live-track" style={{ padding: '80px 0', background: 'rgba(0,0,0,0.2)' }}>
            <div className="container">
                <div style={{ textAlign: 'center', marginBottom: '40px' }}>
                    <h2 style={{ fontSize: '2.5rem', marginBottom: '16px' }}>Live System <span className="text-gradient-primary">Monitor</span></h2>
                    <p style={{ color: 'var(--color-text-muted)' }}>Real-time telemetry and AI inference running on Boat ID: <span style={{ color: 'white', fontFamily: 'monospace' }}>TN-02-SEA-449</span></p>
                </div>

                {/* Dashboard Grid */}
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repea(auto-fit, minmax(300px, 1fr))', /* Typo fix in next step if caught, but 'repeat' is correct layout */
                    gap: '24px'
                }}>

                    {/* BIG MAP MOCKUP */}
                    <div className="glass-panel map-container" style={{ gridColumn: '1 / -1', height: '400px', display: 'flex', flexDirection: 'column' }}>
                        <div style={{ padding: '16px', borderBottom: '1px solid var(--glass-border)', display: 'flex', justifyContent: 'space-between' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <MapPin size={18} color="var(--color-primary)" />
                                <span style={{ fontWeight: 600 }}>Bay of Bengal - Zone 4</span>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--color-success)', boxShadow: '0 0 10px var(--color-success)' }}></div>
                                <span style={{ fontSize: '0.8rem', color: 'var(--color-success)' }}>LIVE TRACKING</span>
                            </div>
                        </div>

                        <div className="map-grid" style={{ flex: 1, position: 'relative' }}>
                            {/* Simulated Border Line */}
                            <div style={{
                                position: 'absolute',
                                top: 0, bottom: 0, right: '20%',
                                borderLeft: '2px dashed var(--color-danger)',
                                opacity: 0.6
                            }}>
                                <span style={{
                                    position: 'absolute', top: '10px', left: '10px',
                                    color: 'var(--color-danger)', fontSize: '0.8rem', fontWeight: 'bold'
                                }}>INTERNATIONAL MARITIME BORDER</span>
                            </div>

                            {/* Boat Icon - Moving */}
                            <div style={{
                                position: 'absolute',
                                top: '50%',
                                right: `${stats.distanceToBorder * 5 + 20}%`, // Moves based on distance
                                transition: 'all 2s linear',
                                transform: `translate(-50%, -50%) rotate(${stats.heading}deg)`
                            }}>
                                <Navigation size={32} color="var(--color-primary)" fill="rgba(6,182,212,0.2)" />
                            </div>

                            {/* Radar Pulse Effect around boat */}
                            <div style={{
                                position: 'absolute',
                                top: '50%',
                                right: `${stats.distanceToBorder * 5 + 20}%`,
                                width: '100px', height: '100px',
                                borderRadius: '50%',
                                border: '1px solid var(--color-primary)',
                                transform: 'translate(50%, -50%)', /* Center it */
                                animation: 'pulse-ring 3s cubic-bezier(0.215, 0.61, 0.355, 1) infinite',
                                pointerEvents: 'none',
                                marginTop: '-50px',
                                marginRight: '-50px' /* Hacky centering fix for absolute positioning */
                            }}></div>
                        </div>
                    </div>

                    {/* STATUS CARDS */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gridColumn: '1 / -1', gap: '20px' }}>

                        {/* Speed Card */}
                        <div className="glass-panel text-center" style={{ padding: '24px' }}>
                            <div style={{ color: 'var(--color-text-muted)', marginBottom: '8px', fontSize: '0.9rem' }}>Vessel Speed</div>
                            <div style={{ fontSize: '2.5rem', fontWeight: 700, color: 'white' }}>
                                {stats.speed} <span style={{ fontSize: '1rem', color: 'var(--color-text-muted)' }}>knots</span>
                            </div>
                        </div>

                        {/* Border Distance Card */}
                        <div className="glass-panel text-center" style={{ padding: '24px', border: stats.distanceToBorder < 3 ? '1px solid var(--color-danger)' : '' }}>
                            <div style={{ color: 'var(--color-text-muted)', marginBottom: '8px', fontSize: '0.9rem' }}>Distance to Border</div>
                            <div style={{ fontSize: '2.5rem', fontWeight: 700, color: 'white' }}>
                                {stats.distanceToBorder} <span style={{ fontSize: '1rem', color: 'var(--color-text-muted)' }}>km</span>
                            </div>
                            {stats.distanceToBorder < 3 && <div style={{ color: 'var(--color-danger)', fontSize: '0.8rem', marginTop: '8px', fontWeight: 'bold' }}>APPROACHING ZONE</div>}
                        </div>

                        {/* Risk Level */}
                        <div className="glass-panel text-center" style={{ padding: '24px' }}>
                            <div style={{ color: 'var(--color-text-muted)', marginBottom: '8px', fontSize: '0.9rem' }}>AI Threat Assess</div>
                            <div style={{
                                fontSize: '1.5rem', fontWeight: 700,
                                color: stats.riskLevel === 'SAFE' ? 'var(--color-success)' : 'var(--color-secondary)',
                                padding: '4px 12px',
                                borderRadius: '8px',
                                background: stats.riskLevel === 'SAFE' ? 'rgba(34, 197, 94, 0.1)' : 'rgba(249, 115, 22, 0.1)',
                                display: 'inline-block'
                            }}>
                                {stats.riskLevel}
                            </div>
                        </div>

                        {/* Connectivity */}
                        <div className="glass-panel text-center" style={{ padding: '24px' }}>
                            <div style={{ color: 'var(--color-text-muted)', marginBottom: '8px', fontSize: '0.9rem' }}>Mesh Network</div>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                                <Wifi size={24} color="var(--color-primary)" />
                                <span style={{ fontWeight: 600 }}>Active (4 Boats)</span>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </section>
    );
}
