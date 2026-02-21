import React from 'react';
import { motion } from 'framer-motion';
import { Users, FileText, CheckSquare, Plus, Video, Calendar } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const TeacherDashboard = () => {
    const navigate = useNavigate();

    return (
        <div className="space-y-8">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold text-white">Teacher Dashboard</h1>
                <p className="text-slate-400 mt-2">Manage your classes and students efficiently.</p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                {[
                    { label: 'Total Students', value: '156', icon: Users, color: 'text-indigo-400', bg: 'bg-indigo-500/10' },
                    { label: 'Assignments', value: '12', icon: FileText, color: 'text-pink-400', bg: 'bg-pink-500/10' },
                    { label: 'Evaluated', value: '88%', icon: CheckSquare, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
                    { label: 'Upcoming', value: '3 Classes', icon: Calendar, color: 'text-amber-400', bg: 'bg-amber-500/10' },
                ].map((stat, i) => (
                    <div key={i} className="glass p-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-slate-400 text-sm font-medium">{stat.label}</p>
                                <h3 className="text-2xl font-bold text-white mt-2">{stat.value}</h3>
                            </div>
                            <div className={`p-3 rounded-lg ${stat.bg}`}>
                                <stat.icon size={20} className={stat.color} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Quick Actions */}
                <div className="lg:col-span-2 space-y-6">
                    <h2 className="text-xl font-bold text-white">Quick Actions</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <button
                            onClick={() => navigate('/classroom/new')}
                            className="glass p-6 text-left hover:border-indigo-500/50 transition-colors group"
                        >
                            <div className="w-12 h-12 rounded-full bg-indigo-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <Video className="text-white" />
                            </div>
                            <h3 className="text-lg font-bold text-white">Start Live Class</h3>
                            <p className="text-slate-400 text-sm mt-1">Begin a live session instantly or schedule for later.</p>
                        </button>
                        <button className="glass p-6 text-left hover:border-emerald-500/50 transition-colors group">
                            <div className="w-12 h-12 rounded-full bg-emerald-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                <FileText className="text-white" />
                            </div>
                            <h3 className="text-lg font-bold text-white">Create Assignment</h3>
                            <p className="text-slate-400 text-sm mt-1">Post new homework or quiz for your students.</p>
                        </button>
                    </div>

                    <h2 className="text-xl font-bold text-white mt-8">Upcoming Classes</h2>
                    <div className="glass overflow-hidden">
                        <table className="w-full text-left text-slate-300">
                            <thead className="bg-slate-800/50 text-slate-400 text-xs uppercase">
                                <tr>
                                    <th className="p-4 font-semibold">Subject</th>
                                    <th className="p-4 font-semibold">Topic</th>
                                    <th className="p-4 font-semibold">Time</th>
                                    <th className="p-4 font-semibold">Status</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-700/50">
                                {[
                                    { sub: 'Physics', topic: 'Thermodynamics', time: 'Today, 2:00 PM', status: 'Scheduled' },
                                    { sub: 'Math', topic: 'Linear Algebra', time: 'Tomorrow, 10:00 AM', status: 'Scheduled' },
                                    { sub: 'Physics', topic: 'Quantum Labs', time: 'Fri, 11:00 AM', status: 'Draft' },
                                ].map((row, i) => (
                                    <tr key={i} className="hover:bg-slate-800/30 transition-colors">
                                        <td className="p-4 font-medium text-white">{row.sub}</td>
                                        <td className="p-4">{row.topic}</td>
                                        <td className="p-4">{row.time}</td>
                                        <td className="p-4">
                                            <span className={`text-xs font-bold px-2 py-1 rounded-md ${row.status === 'Scheduled' ? 'bg-indigo-500/20 text-indigo-300' : 'bg-slate-500/20 text-slate-400'}`}>
                                                {row.status}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Recent Activity */}
                <div className="glass p-6">
                    <h2 className="text-xl font-bold text-white mb-6">Recent Activity</h2>
                    <div className="space-y-6">
                        {[1, 2, 3, 4].map((i) => (
                            <div key={i} className="flex gap-4">
                                <div className="w-2 h-full bg-slate-800 rounded-full relative">
                                    <div className="absolute top-2 left-1/2 -translate-x-1/2 w-3 h-3 bg-indigo-500 rounded-full border-2 border-slate-900"></div>
                                </div>
                                <div className="pb-6 border-l border-slate-700/50 pl-6 -ml-5">
                                    <p className="text-sm text-slate-300"><span className="font-bold text-white">John Doe</span> submitted Physics Assignment.</p>
                                    <p className="text-xs text-slate-500 mt-1">2 mins ago</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TeacherDashboard;
