import React from 'react';
import { ArrowRight, Shield, Activity } from 'lucide-react';

export default function Hero() {
    return (
        <section id="home" style={{
            padding: '160px 0 100px 0',
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            position: 'relative'
        }}>
            <div className="container">
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                    gap: '4rem',
                    alignItems: 'center'
                }}>
                    {/* Content */}
                    <div style={{ maxWidth: '600px' }}>
                        <div style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '8px',
                            padding: '8px 16px',
                            background: 'rgba(6, 182, 212, 0.1)',
                            borderRadius: '20px',
                            color: 'var(--color-primary)',
                            marginBottom: '24px',
                            fontSize: '0.9rem',
                            fontWeight: 600
                        }}>
                            <Shield size={16} />
                            <span>AI-Powered Maritime Protection</span>
                        </div>

                        <h1 style={{
                            fontSize: '3.5rem',
                            lineHeight: 1.1,
                            marginBottom: '24px',
                            fontWeight: 800
                        }}>
                            Navigate Safely with <br />
                            <span className="text-gradient-primary">Intelligent Borders</span>
                        </h1>

                        <p style={{
                            fontSize: '1.25rem',
                            color: 'var(--color-text-muted)',
                            marginBottom: '32px',
                            lineHeight: 1.6
                        }}>
                            Offline-first AI system that predicts border drifts, detects man-overboard incidents, and keeps families connected. Designed for the toughest independent fishermen.
                        </p>

                        <div style={{ display: 'flex', gap: '16px' }}>
                            <button className="glass-button" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                Launch System <ArrowRight size={18} />
                            </button>
                            <button className="glass-button secondary">
                                View Live Demo
                            </button>
                        </div>

                        <div style={{ marginTop: '48px', display: 'flex', gap: '40px' }}>
                            <div>
                                <h3 style={{ fontSize: '2rem', fontWeight: 700, color: 'white' }}>98%</h3>
                                <p style={{ color: 'var(--color-text-muted)' }}>Border Violation Reduction</p>
                            </div>
                            <div>
                                <h3 style={{ fontSize: '2rem', fontWeight: 700, color: 'white' }}>Offline</h3>
                                <p style={{ color: 'var(--color-text-muted)' }}>AI Processing</p>
                            </div>
                        </div>
                    </div>

                    {/* Image/Visual */}
                    <div className="hero-image-container animate-float" style={{ position: 'relative' }}>
                        {/* Glow effect behind */}
                        <div style={{
                            position: 'absolute',
                            inset: 0,
                            background: 'radial-gradient(circle, var(--color-primary-glow) 0%, transparent 70%)',
                            filter: 'blur(40px)',
                            zIndex: -1
                        }}></div>

                        <img
                            src="/assets/dashboard.png"
                            alt="Maritime AI System Interface"
                            style={{
                                width: '100%',
                                borderRadius: '16px',
                                border: '1px solid var(--glass-border)',
                                boxShadow: '0 20px 50px -10px rgba(0,0,0,0.5)'
                            }}
                        />

                        {/* Floating cards */}
                        <div className="glass-panel" style={{
                            position: 'absolute',
                            bottom: '-20px',
                            left: '-20px',
                            padding: '16px',
                            display: 'flex',
                            gap: '12px',
                            alignItems: 'center',
                            animation: 'float 4s ease-in-out infinite reverse'
                        }}>
                            <Activity color="var(--color-secondary)" />
                            <div>
                                <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>Wearable Signal</div>
                                <div style={{ fontWeight: 600 }}>Connected • Stable</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
