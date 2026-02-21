import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    LineChart,
    Clock,
    Calendar,
    CheckCircle,
    Video,
    TrendingUp,
    LogOut,
    ArrowRight
} from 'lucide-react';
import { GlassCard, CountUp } from '../components/Animations';
import { Line, Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

export default function StudentDashboard() {
    const { user, signOut } = useAuth();
    const navigate = useNavigate();

    // Mock Data - In real app, fetch from Supabase
    const attendance = 85;
    const totalHours = 42;
    const nextMeeting = {
        title: "Advanced Mathematics",
        time: "Today, 4:00 PM",
        id: "math-101"
    };

    const performanceData = {
        labels: ['Test 1', 'Test 2', 'Test 3', 'Test 4', 'Test 5'],
        datasets: [
            {
                label: 'Test Score',
                data: [65, 78, 75, 82, 88],
                borderColor: 'rgb(14, 165, 233)', // primary-500
                backgroundColor: 'rgba(14, 165, 233, 0.2)',
                tension: 0.4,
                fill: true,
            }
        ]
    };

    const chartOptions = {
        responsive: true,
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                backgroundColor: 'rgba(30, 41, 59, 0.9)',
                titleColor: '#f8fafc',
                bodyColor: '#f8fafc',
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 1,
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                grid: {
                    color: 'rgba(255, 255, 255, 0.05)',
                },
                ticks: {
                    color: '#94a3b8'
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    color: '#94a3b8'
                }
            }
        }
    };

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: { y: 20, opacity: 0 },
        visible: { y: 0, opacity: 1 }
    };

    return (
        <div className="min-h-screen bg-slate-900 text-white p-6 md:p-10">
            {/* Header */}
            <motion.div
                initial={{ y: -20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className="flex justify-between items-center mb-10"
            >
                <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-tr from-primary-500 to-secondary-500 flex items-center justify-center text-xl font-bold">
                        {user?.email?.[0].toUpperCase() || 'S'}
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold">Hello, {user?.email?.split('@')[0]}</h1>
                        <p className="text-slate-400">Student Dashboard</p>
                    </div>
                </div>
                <button
                    onClick={signOut}
                    className="p-2 hover:bg-slate-800 rounded-lg transition-colors text-slate-400 hover:text-white"
                >
                    <LogOut size={24} />
                </button>
            </motion.div>

            {/* Grid Layout */}
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10"
            >
                {/* Stat Cards */}
                <GlassCard delay={0.1}>
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 bg-primary-500/10 rounded-xl text-primary-400">
                            <CheckCircle size={24} />
                        </div>
                        <span className="text-green-400 text-sm font-medium">+2.5%</span>
                    </div>
                    <h3 className="text-slate-400 text-sm font-medium mb-1">Attendance</h3>
                    <div className="text-3xl font-bold">
                        <CountUp to={attendance} />%
                    </div>
                </GlassCard>

                <GlassCard delay={0.2}>
                    <div className="flex justify-between items-start mb-4">
                        <div className="p-3 bg-secondary-500/10 rounded-xl text-secondary-400">
                            <Clock size={24} />
                        </div>
                    </div>
                    <h3 className="text-slate-400 text-sm font-medium mb-1">Hours Attended</h3>
                    <div className="text-3xl font-bold">
                        <CountUp to={totalHours} />h
                    </div>
                </GlassCard>

                {/* Upcoming Meeting Card - Span 2 cols on large */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3, duration: 0.5 }}
                    className="glass-card p-6 rounded-2xl md:col-span-2 relative overflow-hidden border-l-4 border-l-primary-500 group"
                >
                    <div className="absolute inset-0 bg-gradient-to-r from-primary-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                    <div className="flex flex-col sm:flex-row justify-between items-center h-full gap-4 relative z-10">
                        <div>
                            <div className="flex items-center gap-2 text-primary-400 mb-2">
                                <Video size={20} className="animate-pulse" />
                                <span className="text-sm font-semibold uppercase tracking-wider">Upcoming Class</span>
                            </div>
                            <h3 className="text-2xl font-bold mb-1">{nextMeeting.title}</h3>
                            <p className="text-slate-400 flex items-center gap-2">
                                <Calendar size={16} />
                                {nextMeeting.time}
                            </p>
                        </div>
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => navigate(`/meeting/${nextMeeting.id}`)}
                            className="px-6 py-3 bg-primary-600 hover:bg-primary-500 text-white rounded-xl font-semibold shadow-lg shadow-primary-900/20 transition-all active:scale-95 w-full sm:w-auto flex items-center gap-2"
                        >
                            Join Class Now <ArrowRight size={18} />
                        </motion.button>
                    </div>
                </motion.div>
            </motion.div>

            {/* Charts Section */}
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="grid grid-cols-1 lg:grid-cols-2 gap-6"
            >
                <motion.div variants={itemVariants} className="glass-card p-6 rounded-2xl">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-lg font-bold flex items-center gap-2">
                            <TrendingUp size={20} className="text-green-400" />
                            Performance Overview
                        </h3>
                    </div>
                    <div className="h-[300px] w-full">
                        <Line options={chartOptions} data={performanceData} />
                    </div>
                </motion.div>

                <motion.div variants={itemVariants} className="glass-card p-6 rounded-2xl">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-lg font-bold">Recent Test Scores</h3>
                    </div>
                    {/* List of recent tests */}
                    <div className="space-y-4">
                        {[
                            { name: 'Physics Quiz', score: 88, date: 'Jan 20, 2026' },
                            { name: 'Math Midterm', score: 82, date: 'Jan 15, 2026' },
                            { name: 'English Essay', score: 75, date: 'Jan 10, 2026' },
                        ].map((test, i) => (
                            <div key={i} className="flex items-center justify-between p-4 bg-slate-800/40 rounded-xl hover:bg-slate-800/60 transition-colors cursor-pointer">
                                <div>
                                    <h4 className="font-semibold">{test.name}</h4>
                                    <p className="text-xs text-slate-500">{test.date}</p>
                                </div>
                                <div className={`text-lg font-bold ${test.score >= 80 ? 'text-green-400' : test.score >= 60 ? 'text-yellow-400' : 'text-red-400'}`}>
                                    {test.score}%
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.div>
            </motion.div>
        </div>
    );
}
