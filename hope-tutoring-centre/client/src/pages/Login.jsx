import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Mail, Lock, Loader2, ArrowRight } from 'lucide-react';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const { signIn, role } = useAuth(); // role here might be null initially
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            await doLogin(email, password);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    const doLogin = async (loginEmail, loginPassword) => {
        try {
            const { user } = await signIn(loginEmail, loginPassword);

            // Explicitly navigate based on the role determined by email for demo
            // or wait for context update. To be safe/fast for demo purposes:
            if (loginEmail.includes('teacher')) {
                navigate('/teacher-dashboard');
            } else {
                navigate('/student-dashboard');
            }
        } catch (err) {
            throw err;
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900 relative overflow-hidden">
            {/* Premium Animated Background */}
            <div className="absolute inset-0 overflow-hidden z-0">
                <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_50%_50%,_rgba(15,23,42,0.9),_rgba(15,23,42,1))]"></div>

                {/* Floating Orbs */}
                <motion.div
                    animate={{
                        y: [0, -50, 0],
                        x: [0, 30, 0],
                        scale: [1, 1.2, 1],
                    }}
                    transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
                    className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-primary-600/20 rounded-full blur-[100px]"
                />
                <motion.div
                    animate={{
                        y: [0, 50, 0],
                        x: [0, -30, 0],
                        scale: [1, 1.1, 1],
                    }}
                    transition={{ duration: 15, repeat: Infinity, ease: "easeInOut", delay: 1 }}
                    className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-secondary-600/20 rounded-full blur-[100px]"
                />
                <motion.div
                    animate={{
                        y: [0, -30, 0],
                        opacity: [0.3, 0.6, 0.3]
                    }}
                    transition={{ duration: 8, repeat: Infinity }}
                    className="absolute top-[40%] left-[20%] w-[300px] h-[300px] bg-blue-500/10 rounded-full blur-[80px]"
                />
            </div>

            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, type: "spring", bounce: 0.4 }}
                className="glass p-8 rounded-2xl w-full max-w-md relative z-10 shadow-2xl border-t border-white/10"
            >
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
                    <p className="text-gray-400">Sign in to Hope Tutoring Centre</p>
                </div>

                {error && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        className="bg-red-500/10 border border-red-500/50 text-red-200 p-3 rounded-lg mb-6 text-sm"
                    >
                        {error}
                    </motion.div>
                )}

                <form onSubmit={handleLogin} className="space-y-6">
                    <div className="relative group">
                        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-primary-400 transition-colors w-5 h-5" />
                        <input
                            type="email"
                            placeholder="Email Address"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full bg-slate-800/50 border border-slate-700 rounded-xl py-3 pl-10 pr-4 text-white placeholder-gray-500 focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all"
                            required
                        />
                    </div>

                    <div className="relative group">
                        <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-secondary-400 transition-colors w-5 h-5" />
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full bg-slate-800/50 border border-slate-700 rounded-xl py-3 pl-10 pr-4 text-white placeholder-gray-500 focus:ring-2 focus:ring-secondary-500/50 focus:border-secondary-500 transition-all"
                            required
                        />
                    </div>

                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        type="submit"
                        disabled={loading}
                        className="w-full bg-gradient-to-r from-primary-600 to-secondary-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-primary-500/25 transition-all flex items-center justify-center gap-2 group"
                    >
                        {loading ? (
                            <Loader2 className="w-5 h-5 animate-spin" />
                        ) : (
                            <>
                                Sign In
                                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                            </>
                        )}
                    </motion.button>
                </form>

                <div className="mt-8 pt-6 border-t border-slate-700/50">
                    <p className="text-gray-500 text-sm text-center mb-4">Quick Demo Access (No password needed)</p>
                    <div className="grid grid-cols-2 gap-4">
                        <button
                            onClick={() => doLogin('student.demo@hope.com', 'pass')}
                            className="bg-slate-800 hover:bg-slate-700 text-primary-400 text-xs font-semibold py-2 px-4 rounded-lg transition-colors border border-slate-700"
                        >
                            Demo Student
                        </button>
                        <button
                            onClick={() => doLogin('teacher.demo@hope.com', 'pass')}
                            className="bg-slate-800 hover:bg-slate-700 text-secondary-400 text-xs font-semibold py-2 px-4 rounded-lg transition-colors border border-slate-700"
                        >
                            Demo Teacher
                        </button>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
