import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
    LayoutDashboard,
    Video,
    BookOpen,
    FileCheck,
    BarChart2,
    Settings,
    Users,
    LogOut
} from 'lucide-react';

const Sidebar = () => {
    const { user, logout } = useAuth();

    if (!user) return null;

    const getLinks = () => {
        switch (user.role) {
            case 'student':
                return [
                    { icon: LayoutDashboard, label: 'Dashboard', path: '/student/dashboard' },
                    { icon: Video, label: 'Live Classes', path: '/student/classes' },
                    { icon: BookOpen, label: 'Assignments', path: '/student/assignments' },
                    { icon: FileCheck, label: 'Tests', path: '/student/tests' },
                    { icon: BarChart2, label: 'Performance', path: '/student/performance' },
                ];
            case 'teacher':
                return [
                    { icon: LayoutDashboard, label: 'Dashboard', path: '/teacher/dashboard' },
                    { icon: Video, label: 'My Classes', path: '/teacher/classes' },
                    { icon: BookOpen, label: 'Assignments', path: '/teacher/assignments' },
                    { icon: Users, label: 'Students', path: '/teacher/students' },
                    { icon: BarChart2, label: 'Reports', path: '/teacher/reports' },
                ];
            case 'admin':
                return [
                    { icon: LayoutDashboard, label: 'Dashboard', path: '/admin/dashboard' },
                    { icon: Users, label: 'Manage Users', path: '/admin/users' },
                    { icon: Settings, label: 'Settings', path: '/admin/settings' },
                ];
            default:
                return [];
        }
    };

    const links = getLinks();

    return (
        <div className="h-screen w-64 glass-panel flex flex-col fixed left-0 top-0 z-50 transition-all duration-300">
            <div className="p-6 flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center font-bold text-xl">H</div>
                <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">HOPE</span>
            </div>

            <nav className="flex-1 px-4 py-4 space-y-2">
                {links.map((link) => (
                    <NavLink
                        key={link.path}
                        to={link.path}
                        className={({ isActive }) =>
                            `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group ${isActive
                                ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 shadow-[0_0_15px_rgba(99,102,241,0.3)]'
                                : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
                            }`
                        }
                    >
                        <link.icon size={20} className="transition-transform group-hover:scale-110" />
                        <span className="font-medium">{link.label}</span>
                    </NavLink>
                ))}
            </nav>

            <div className="p-4 border-t border-slate-700/50">
                <div className="flex items-center gap-3 mb-4 px-2">
                    <img src={user.avatar} alt="User" className="w-10 h-10 rounded-full border-2 border-indigo-500/50" />
                    <div className="overflow-hidden">
                        <p className="font-medium text-sm truncate text-slate-200">{user.name}</p>
                        <p className="text-xs text-slate-500 capitalize">{user.role}</p>
                    </div>
                </div>
                <button
                    onClick={logout}
                    className="w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-colors"
                >
                    <LogOut size={18} />
                    <span>Logout</span>
                </button>
            </div>
        </div>
    );
};

export default Sidebar;
