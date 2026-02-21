import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

const Layout = () => {
    return (
        <div className="min-h-screen bg-slate-900 text-slate-100 flex">
            <Sidebar />
            <main className="flex-1 ml-64 p-8 overflow-y-auto h-screen relative">
                <div className="absolute inset-0 pointer-events-none z-0">
                    <div className="absolute top-0 left-0 w-full h-96 bg-gradient-to-b from-indigo-900/20 to-transparent opacity-50"></div>
                    <div className="absolute -top-24 -right-24 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
                    <div className="absolute top-1/2 left-1/4 w-64 h-64 bg-emerald-500/5 rounded-full blur-3xl"></div>
                </div>
                <div className="relative z-10 max-w-7xl mx-auto fade-in">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default Layout;
