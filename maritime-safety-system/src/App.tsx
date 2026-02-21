import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import LiveDashboard from './components/LiveDashboard';
import Features from './components/Features';
import Footer from './components/Footer';

function App() {
    return (
        <div className="app-container">
            <Navbar />
            <main>
                <Hero />
                <LiveDashboard />
                <Features />
            </main>
            <Footer />
        </div>
    );
}

export default App;
