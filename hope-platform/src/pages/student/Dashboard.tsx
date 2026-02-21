import React from 'react';
import { motion } from 'framer-motion';
import { Play, Clock, FileText, TrendingUp, CheckCircle, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const StudentDashboard = () => {
    const navigate = useNavigate();
    const stats = [
        { title: 'Attendance', value: '92%', change: '+2%', icon: CheckCircle, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
        { title: 'Avg Score', value: '85/100', change: '+5', icon: TrendingUp, color: 'text-indigo-400', bg: 'bg-indigo-500/10' },
        { title: 'Pending', value: '3 Tasks', change: 'Due Soon', icon: AlertCircle, color: 'text-amber-400', bg: 'bg-amber-500/10' },
    ];

    const liveClasses = [
        { id: 1, subject: 'Advanced Physics', title: 'Quantum Mechanics Ep. 3', teacher: 'Dr. Sarah Smith', time: 'LIVE', viewers: 24, thumbnail: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=600&auto=format&fit=crop' },
        { id: 2, subject: 'Mathematics', title: 'Calculus III: Integration', teacher: 'Prof. John Doe', time: '10:30 AM', viewers: 0, thumbnail: 'https://images.unsplash.com/photo-1596495578065-6e0763fa1178?q=80&w=600&auto=format&fit=crop' },
    ];

    const chartData = {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        datasets: [{
            label: 'Performance',
            data: [65, 78, 82, 75, 88, 92],
            fill: true,
            borderColor: 'rgb(99, 102, 241)',
            backgroundColor: 'rgba(99, 102, 241, 0.1)',
            tension: 0.4
        }]
    };

    const chartOptions = {
        responsive: true,
        plugins: {
            legend: { display: false },
            tooltip: {
                mode: 'index' as const,
                intersect: false,
                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                titleColor: '#f8fafc',
                bodyColor: '#cbd5e1',
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 1
            }
        },
        scales: {
            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
        }
    };

    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">Student Dashboard</h1>
                    <p className="text-slate-400 mt-2">Welcome back, continue your learning journey</p>
                </div>
                <div className="text-right hidden md:block">
                    <p className="text-2xl font-bold text-white">10:42 AM</p>
                    <p className="text-slate-500 text-sm">Wednesday, Jan 24</p>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {stats.map((stat, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="glass p-6 flex items-center justify-between"
                    >
                        <div>
                            <p className="text-slate-400 text-sm font-medium mb-1">{stat.title}</p>
                            <h3 className="text-2xl font-bold text-white">{stat.value}</h3>
                            <span className={`text-xs font-medium ${stat.color} bg-opacity-20 px-2 py-1 rounded-full mt-2 inline-block`}>
                                {stat.change}
                            </span>
                        </div>
                        <div className={`p-3 rounded-xl ${stat.bg}`}>
                            <stat.icon size={24} className={stat.color} />
                        </div>
                    </motion.div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Live Classes - Span 2 cols */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="flex justify-between items-center">
                        <h2 className="text-xl font-bold text-white flex items-center gap-2">
                            <VideoIcon /> Live Classes
                        </h2>
                        <button className="text-sm text-indigo-400 hover:text-indigo-300">View All</button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {liveClasses.map((cls) => (
                            <div
                                key={cls.id}
                                onClick={() => navigate(`/classroom/${cls.id}`)}
                                className="group glass overflow-hidden hover:border-indigo-500/50 transition-all cursor-pointer"
                            >
                                <div className="relative h-40">
                                    <img src={cls.thumbnail} alt={cls.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                                    <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent opacity-80"></div>
                                    {cls.time === 'LIVE' ? (
                                        <span className="absolute top-3 left-3 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-md animate-pulse flex items-center gap-1">
                                            <span className="w-2 h-2 bg-white rounded-full"></span> LIVE
                                        </span>
                                    ) : (
                                        <span className="absolute top-3 left-3 bg-slate-800/80 backdrop-blur text-white text-xs font-bold px-2 py-1 rounded-md flex items-center gap-1">
                                            <Clock size={12} /> {cls.time}
                                        </span>
                                    )}
                                    <button className="absolute bottom-3 right-3 w-10 h-10 bg-indigo-600 rounded-full flex items-center justify-center text-white shadow-lg transform translate-y-10 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all">
                                        <Play size={20} fill="currentColor" />
                                    </button>
                                </div>
                                <div className="p-4">
                                    <p className="text-indigo-400 text-xs font-semibold mb-1 uppercase tracking-wider">{cls.subject}</p>
                                    <h3 className="text-white font-bold mb-1 truncate">{cls.title}</h3>
                                    <p className="text-slate-400 text-sm">{cls.teacher}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Analytics Chart */}
                <div className="glass p-6 flex flex-col">
                    <h2 className="text-xl font-bold text-white mb-6">Performance Trend</h2>
                    <div className="flex-1 w-full min-h-[250px] relative">
                        <Line data={chartData} options={chartOptions} />
                    </div>
                </div>
            </div>
        </div>
    );
};

const VideoIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-indigo-500"><path d="m22 8-6 4 6 4V8Z" /><rect width="14" height="12" x="2" y="6" rx="2" ry="2" /></svg>
);

export default StudentDashboard;
