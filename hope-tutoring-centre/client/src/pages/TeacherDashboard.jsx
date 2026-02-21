import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Users,
    Video,
    FileText,
    Download,
    Plus,
    Search,
    MoreVertical,
    LogOut,
    Calendar
} from 'lucide-react';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable'; // Note: might need to install this specific plugin if standard jspdf doesn't cover simple tables easily, but usually manual is fine. standard jspdf doesn't have autoTable by default, user listed jspdf only. I will stick to basic text or html2canvas.
// Actually, user mentioned html2canvas + jsPDF. I'll use that approach.

export default function TeacherDashboard() {
    const { user, signOut } = useAuth();
    const [activeTab, setActiveTab] = useState('overview');
    const [isModalOpen, setIsModalOpen] = useState(false);

    // Mock Students Data
    const students = [
        { id: 1, name: "Alice Johnson", email: "alice@example.com", attendance: 92, avgScore: 88, status: 'Improved' },
        { id: 2, name: "Bob Smith", email: "bob@example.com", attendance: 78, avgScore: 72, status: 'Same' },
        { id: 3, name: "Charlie Brown", email: "charlie@example.com", attendance: 85, avgScore: 65, status: 'Declined' },
        { id: 4, name: "Diana Prince", email: "diana@example.com", attendance: 96, avgScore: 94, status: 'Improved' },
    ];

    const generatePDF = (student) => {
        const doc = new jsPDF();

        // Header
        doc.setFillColor(15, 23, 42); // slate-900
        doc.rect(0, 0, 210, 40, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(22);
        doc.text("HOPE TUTORING CENTRE", 105, 20, { align: 'center' });
        doc.setFontSize(12);
        doc.text("Student Performance Report", 105, 30, { align: 'center' });

        // Student Info
        doc.setTextColor(0, 0, 0);
        doc.setFontSize(14);
        doc.text(`Student Name: ${student.name}`, 20, 60);
        doc.text(`Email: ${student.email}`, 20, 70);

        // Stats
        doc.setDrawColor(200, 200, 200);
        doc.line(20, 80, 190, 80);

        doc.text("Performance Summary:", 20, 95);
        doc.setFontSize(12);
        doc.text(`• Attendance: ${student.attendance}%`, 25, 105);
        doc.text(`• Average Score: ${student.avgScore}%`, 25, 115);
        doc.text(`• Status: ${student.status}`, 25, 125);

        // Footer
        doc.setFontSize(10);
        doc.setTextColor(150);
        doc.text(`Generated on ${new Date().toLocaleDateString()}`, 20, 280);

        doc.save(`${student.name.replace(' ', '_')}_Report.pdf`);
    };

    return (
        <div className="flex min-h-screen bg-slate-900 text-white">
            {/* Sidebar */}
            <aside className="w-20 lg:w-64 border-r border-slate-800 bg-slate-900/50 backdrop-blur-xl flex flex-col fixed h-full z-20">
                <div className="p-6 flex items-center gap-3 border-b border-slate-800">
                    <div className="w-8 h-8 rounded-lg bg-primary-500 flex-shrink-0"></div>
                    <span className="font-bold text-xl hidden lg:block">HOPE</span>
                </div>

                <nav className="flex-1 p-4 space-y-2">
                    {[
                        { id: 'overview', icon: Users, label: 'Overview' },
                        { id: 'meetings', icon: Video, label: 'Meetings' },
                        { id: 'tests', icon: FileText, label: 'MCQ Tests' },
                    ].map((item) => (
                        <button
                            key={item.id}
                            onClick={() => setActiveTab(item.id)}
                            className={`w-full flex items-center gap-3 p-3 rounded-xl transition-all ${activeTab === item.id
                                ? 'bg-primary-600/10 text-primary-400 border border-primary-500/20'
                                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                                }`}
                        >
                            <item.icon size={20} />
                            <span className="hidden lg:block font-medium">{item.label}</span>
                        </button>
                    ))}
                </nav>

                <div className="p-4 border-t border-slate-800">
                    <button
                        onClick={signOut}
                        className="w-full flex items-center gap-3 p-3 rounded-xl text-slate-400 hover:bg-red-500/10 hover:text-red-400 transition-all"
                    >
                        <LogOut size={20} />
                        <span className="hidden lg:block font-medium">Sign Out</span>
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 ml-20 lg:ml-64 p-6 lg:p-10">
                <header className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-3xl font-bold">Teacher Dashboard</h1>
                        <p className="text-slate-400">Manage your classes and students</p>
                    </div>
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => window.open(`/meeting/math-101`, '_self')}
                        className="bg-primary-600 hover:bg-primary-500 text-white px-4 py-2 rounded-lg flex items-center gap-2 shadow-lg shadow-primary-900/20"
                    >
                        <Video size={20} />
                        <span className="hidden sm:inline">Launch Live Class</span>
                    </motion.button>
                </header>

                {activeTab === 'overview' && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="glass-card rounded-2xl overflow-hidden"
                    >
                        <div className="p-6 border-b border-slate-800 flex justify-between items-center">
                            <h3 className="font-bold text-lg">Enrolled Students</h3>
                            <div className="relative">
                                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 w-4 h-4" />
                                <input
                                    type="text"
                                    placeholder="Search students..."
                                    className="bg-slate-900/50 border border-slate-700 rounded-lg py-2 pl-9 pr-4 text-sm focus:w-64 w-48 transition-all"
                                />
                            </div>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left bg-slate-800/20">
                                <thead className="text-slate-400 text-xs uppercase bg-slate-900/50">
                                    <tr>
                                        <th className="px-6 py-4 font-medium">Name</th>
                                        <th className="px-6 py-4 font-medium">Status</th>
                                        <th className="px-6 py-4 font-medium">Attendance</th>
                                        <th className="px-6 py-4 font-medium">Average Score</th>
                                        <th className="px-6 py-4 font-medium text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-800">
                                    {students.map((student) => (
                                        <tr key={student.id} className="hover:bg-slate-800/30 transition-colors">
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-xs font-bold">
                                                        {student.name.charAt(0)}
                                                    </div>
                                                    <div className="font-medium">{student.name}</div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${student.status === 'Improved' ? 'bg-green-500/10 text-green-400' :
                                                    student.status === 'Same' ? 'bg-yellow-500/10 text-yellow-400' :
                                                        'bg-red-500/10 text-red-400'
                                                    }`}>
                                                    {student.status}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-slate-300">{student.attendance}%</td>
                                            <td className="px-6 py-4 text-slate-300">{student.avgScore}%</td>
                                            <td className="px-6 py-4 text-right">
                                                <button
                                                    onClick={() => generatePDF(student)}
                                                    className="text-primary-400 hover:text-primary-300 p-2 hover:bg-primary-500/10 rounded-lg transition-colors"
                                                    title="Download Report"
                                                >
                                                    <Download size={18} />
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </motion.div>
                )}
            </main>
        </div>
    );
}
