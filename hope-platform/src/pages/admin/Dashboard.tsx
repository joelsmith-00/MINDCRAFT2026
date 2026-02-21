import React from 'react';
import { Shield, Users, Server, AlertTriangle, Check, X } from 'lucide-react';

const AdminDashboard = () => {
    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-white">Admin Control Panel</h1>
                <p className="text-slate-400 mt-2">System overview and user management.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="glass p-6 border-l-4 border-indigo-500">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-400 mb-1">Total Users</p>
                            <h2 className="text-3xl font-bold text-white">1,248</h2>
                        </div>
                        <Users size={32} className="text-indigo-500" />
                    </div>
                </div>
                <div className="glass p-6 border-l-4 border-emerald-500">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-400 mb-1">System Health</p>
                            <h2 className="text-3xl font-bold text-white">99.9%</h2>
                        </div>
                        <Server size={32} className="text-emerald-500" />
                    </div>
                </div>
                <div className="glass p-6 border-l-4 border-amber-500">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-slate-400 mb-1">Security Alerts</p>
                            <h2 className="text-3xl font-bold text-white">0</h2>
                        </div>
                        <Shield size={32} className="text-amber-500" />
                    </div>
                </div>
            </div>

            <div className="glass p-6">
                <h2 className="text-xl font-bold text-white mb-6">Pending Teacher Approvals</h2>
                <div className="space-y-4">
                    {[
                        { name: 'Alice Walker', subject: 'Biology', email: 'alice@example.com' },
                        { name: 'Robert Brown', subject: 'Chemistry', email: 'robert@example.com' },
                    ].map((teacher, i) => (
                        <div key={i} className="flex items-center justify-between p-4 bg-slate-800/50 rounded-xl border border-slate-700">
                            <div className="flex items-center gap-4">
                                <div className="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center font-bold text-slate-300">
                                    {teacher.name[0]}
                                </div>
                                <div>
                                    <h3 className="font-bold text-white">{teacher.name}</h3>
                                    <p className="text-sm text-slate-400">{teacher.subject} • {teacher.email}</p>
                                </div>
                            </div>
                            <div className="flex gap-2">
                                <button className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg hover:bg-emerald-500/20 transition-colors">
                                    <Check size={20} />
                                </button>
                                <button className="p-2 bg-red-500/10 text-red-400 rounded-lg hover:bg-red-500/20 transition-colors">
                                    <X size={20} />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;
