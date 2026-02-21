import React from 'react';
import { Shield, CloudOff, Cpu, Anchor, Bell, Users } from 'lucide-react';

const features = [
    {
        icon: <CloudOff size={32} />,
        title: "Offline-First AI",
        desc: "Neural networks run locally on the device. No internet required for border prediction or risk assessment."
    },
    {
        icon: <Cpu size={32} />,
        title: "Border Predictor",
        desc: "Regression models analyze speed & heading to predict violations 30 mins in advance with 98% accuracy."
    },
    {
        icon: <Bell size={32} />,
        title: "Tamil Voice Alerts",
        desc: "Native language synthesis provides urgent warnings for low-literacy users in high-stress situations."
    },
    {
        icon: <Anchor size={32} />,
        title: "Smart Anchoring",
        desc: "Drift detection specifically tuned for fishing vessels to prevent accidental cross-border drift while sleeping."
    },
    {
        icon: <Users size={32} />,
        title: "Family Connect",
        desc: "Emotion-aware status updates sent to family members automatically via SMS/Satellite when signal is available."
    },
    {
        icon: <Shield size={32} />,
        title: "Mesh Safety Net",
        desc: "Boat-to-boat communication creates a safety mesh network extending up to 50km offshore."
    }
];

export default function Features() {
    return (
        <section id="features" style={{ padding: '100px 0', position: 'relative' }}>
            <div className="container">
                <div style={{ textAlign: 'center', marginBottom: '60px' }}>
                    <h2 style={{ fontSize: '2.5rem', marginBottom: '16px' }}>Core <span className="text-gradient-primary">Capabilities</span></h2>
                    <p style={{ color: 'var(--color-text-muted)', maxWidth: '600px', margin: '0 auto' }}>
                        Built for the harshest conditions. Our technology saves lives where connection fails.
                    </p>
                </div>

                <div className="grid-cols-auto">
                    {features.map((feature, index) => (
                        <div key={index} className="glass-panel" style={{
                            padding: '32px',
                            transition: 'transform 0.3s ease',
                            cursor: 'default'
                        }}
                            onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-5px)'}
                            onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
                        >
                            <div style={{
                                width: '60px', height: '60px',
                                background: 'rgba(6, 182, 212, 0.1)',
                                borderRadius: '12px',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                color: 'var(--color-primary)',
                                marginBottom: '24px'
                            }}>
                                {feature.icon}
                            </div>
                            <h3 style={{ fontSize: '1.25rem', marginBottom: '12px', fontWeight: 600 }}>{feature.title}</h3>
                            <p style={{ color: 'var(--color-text-muted)', lineHeight: 1.6 }}>{feature.desc}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}
