import React, { useState, useEffect } from 'react';
import { Anchor, Menu, X, Radio } from 'lucide-react';

export default function Navbar() {
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <nav style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            zIndex: 1000,
            transition: 'all 0.3s ease',
            backgroundColor: isScrolled ? 'rgba(15, 23, 42, 0.9)' : 'transparent',
            backdropFilter: isScrolled ? 'blur(10px)' : 'none',
            borderBottom: isScrolled ? '1px solid rgba(255,255,255,0.1)' : 'none',
            padding: '0 20px'
        }}>
            <div className="container" style={{
                height: '80px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
            }}>
                <div className="flex-center" style={{ gap: '12px' }}>
                    <div style={{ position: 'relative', display: 'flex' }}>
                        <Anchor size={32} color="var(--color-primary)" />
                        <div style={{
                            position: 'absolute',
                            top: '-2px',
                            right: '-2px',
                            width: '10px',
                            height: '10px',
                            backgroundColor: 'var(--color-secondary)',
                            borderRadius: '50%',
                            animation: 'pulse-dot 2s infinite'
                        }}></div>
                    </div>
                    <span style={{ fontSize: '1.5rem', fontWeight: 700, letterSpacing: '1px' }}>
                        SEA<span style={{ color: 'var(--color-primary)' }}>GUARD</span>
                    </span>
                </div>

                {/* Desktop Menu */}
                <div className="desktop-menu" style={{ display: 'flex', gap: '30px', alignItems: 'center' }}>
                    <a href="#home" className="nav-link">Home</a>
                    <a href="#features" className="nav-link">Safety AI</a>
                    <a href="#live-track" className="nav-link" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Radio size={16} color="var(--color-success)" />
                        Live Monitor
                    </a>
                    <a href="#family" className="nav-link">Family Connect</a>
                    <button className="glass-button secondary" style={{ fontSize: '0.9rem', padding: '10px 20px' }}>
                        SOS Emergency
                    </button>
                </div>

                {/* Mobile Toggle (Hidden for now as we focus on desktop logic for MVP/Hackathon view) */}
            </div>

            <style>{`
        @media (max-width: 768px) {
          .desktop-menu { display: none !important; }
        }
      `}</style>
        </nav>
    );
}
