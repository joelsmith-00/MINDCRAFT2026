import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Role } from '../types';
import { BookOpen, Shield, GraduationCap, Users } from 'lucide-react';

const Login = () => {
    const { login } = useAuth();
    const navigate = useNavigate();
    const [role, setRole] = useState<Role>('student');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        // Simulate network delay
        setTimeout(() => {
            login(email || `${role}@hope.edu`, role);
            navigate(`/${role}/dashboard`);
            setLoading(false);
        }, 1000);
    };

    return (
        <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4 relative overflow-hidden">
            {/* Background blobs */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute -top-40 -left-40 w-96 h-96 bg-purple-500/20 rounded-full blur-[100px]"></div>
                <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-indigo-500/20 rounded-full blur-[120px]"></div>
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full max-w-4xl grid md:grid-cols-2 bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl overflow-hidden shadow-2xl"
            >
                {/* Left Side - Info */}
                <div className="p-12 flex flex-col justify-between bg-gradient-to-br from-indigo-900/40 to-slate-900/40 relative">
                    <div>
                        <div className="flex items-center gap-3 mb-8">
                            <div className="w-12 h-12 rounded-xl bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
                                <BookOpen className="text-white" size={24} />
                            </div>
                            <h1 className="text-3xl font-bold text-white tracking-tight">HOPE</h1>
                        </div>

                        <h2 className="text-2xl font-semibold text-slate-200 mb-4">
                            All-in-One Education Platform
                        </h2>
                        <p className="text-slate-400 leading-relaxed">
                            Experience the future of learning with live classes, instant analytics, and seamless management.
                        </p>
                    </div>

                    <div className="mt-12 space-y-4">
                        <div className="flex items-center gap-4 text-slate-300">
                            <div className="p-2 bg-slate-700/50 rounded-lg"><GraduationCap size={20} className="text-emerald-400" /></div>
                            <span>For Students</span>
                        </div>
                        <div className="flex items-center gap-4 text-slate-300">
                            <div className="p-2 bg-slate-700/50 rounded-lg"><Users size={20} className="text-blue-400" /></div>
                            <span>For Teachers</span>
                        </div>
                        <div className="flex items-center gap-4 text-slate-300">
                            <div className="p-2 bg-slate-700/50 rounded-lg"><Shield size={20} className="text-purple-400" /></div>
                            <span>For Admins</span>
                        </div>
                    </div>
                </div>

                {/* Right Side - Form */}
                <div className="p-12 flex flex-col justify-center bg-slate-900/60">
                    <h3 className="text-2xl font-bold text-white mb-6">Welcome Back</h3>

                    <div className="flex p-1 bg-slate-800 rounded-xl mb-8 border border-slate-700">
                        {(['student', 'teacher', 'admin'] as Role[]).map((r) => (
                            <button
                                key={r}
                                onClick={() => setRole(r)}
                                className={`flex-1 py-2 text-sm font-medium rounded-lg capitalize transition-all ${role === r
                                        ? 'bg-indigo-600 text-white shadow-lg'
                                        : 'text-slate-400 hover:text-slate-200'
                                    }`}
                            >
                                {r}
                            </button>
                        ))}
                    </div>

                    <form onSubmit={handleLogin} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-slate-400 mb-1">Email Address</label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder={`${role}@hope.edu`}
                                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-400 mb-1">Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-slate-200 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3.5 rounded-xl shadow-lg shadow-indigo-500/25 transition-all active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed mt-4"
                        >
                            {loading ? (
                                <span className="flex items-center justify-center gap-2">
                                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                                    Signing in...
                                </span>
                            ) : 'Sign In'}
                        </button>
                    </form>

                    <p className="mt-6 text-center text-sm text-slate-500">
                        Don't have an account? <span className="text-indigo-400 hover:underline cursor-pointer">Contact Admin</span>
                    </p>
                </div>
            </motion.div>
        </div>
    );
};

export default Login;
