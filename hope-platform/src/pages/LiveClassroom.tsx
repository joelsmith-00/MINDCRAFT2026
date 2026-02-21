import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Mic, Video, PhoneOff, MessageSquare, Users, Share, Settings } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const LiveClassroom = () => {
    const navigate = useNavigate();
    const [chatOpen, setChatOpen] = useState(true);

    return (
        <div className="h-[calc(100vh-2rem)] flex gap-4 overflow-hidden">
            {/* Main Video Area */}
            <div className="flex-1 flex flex-col gap-4">
                <div className="flex-1 bg-black rounded-2xl relative overflow-hidden group border border-slate-700 shadow-2xl">
                    {/* Main Feed */}
                    <img
                        src="https://images.unsplash.com/photo-1596495578079-b6496912356c?q=80&w=1200&auto=format&fit=crop"
                        alt="Teacher"
                        className="w-full h-full object-cover opacity-80"
                    />

                    <div className="absolute top-6 left-6 flex items-center gap-3">
                        <span className="bg-red-600 text-white text-xs font-bold px-3 py-1 rounded-full animate-pulse flex items-center gap-2">
                            <span className="w-2 h-2 bg-white rounded-full"></span> LIVE
                        </span>
                        <span className="bg-black/50 backdrop-blur text-white text-sm font-medium px-3 py-1 rounded-full border border-white/10">
                            Advanced Physics • Dr. Sarah Smith
                        </span>
                    </div>

                    {/* Controls Bar */}
                    <div className="absolute bottom-8 left-1/2 -translate-x-1/2 bg-slate-900/90 backdrop-blur-xl border border-white/10 px-6 py-3 rounded-2xl flex items-center gap-6 shadow-xl transform transition-transform translate-y-20 group-hover:translate-y-0">
                        <button className="p-3 rounded-full bg-slate-800 hover:bg-slate-700 text-white transition-colors"><Mic size={20} /></button>
                        <button className="p-3 rounded-full bg-slate-800 hover:bg-slate-700 text-white transition-colors"><Video size={20} /></button>
                        <button
                            onClick={() => navigate(-1)}
                            className="px-6 py-3 rounded-full bg-red-600 hover:bg-red-700 text-white font-bold transition-colors flex items-center gap-2"
                        >
                            <PhoneOff size={20} /> End
                        </button>
                        <button className="p-3 rounded-full bg-slate-800 hover:bg-slate-700 text-white transition-colors"><Share size={20} /></button>
                        <button className="p-3 rounded-full bg-slate-800 hover:bg-slate-700 text-white transition-colors"><Settings size={20} /></button>
                    </div>
                </div>
            </div>

            {/* Sidebar (Chat) */}
            <motion.div
                initial={{ width: 320, opacity: 1 }}
                animate={{ width: chatOpen ? 320 : 0, opacity: chatOpen ? 1 : 0 }}
                className="bg-slate-800/50 backdrop-blur-xl border border-slate-700 rounded-2xl flex flex-col overflow-hidden"
            >
                <div className="p-4 border-b border-slate-700 flex items-center justify-between">
                    <h3 className="font-bold text-white">Live Chat</h3>
                    <Users size={16} className="text-slate-400" />
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {[
                        { user: 'Alex', msg: 'Is this clear?' },
                        { user: 'Sam', msg: 'Yes, understood.' },
                        { user: 'Jordan', msg: 'Can you repeat the last part?' },
                        { user: 'Teacher', msg: 'Sure, let me explain again.', role: 'teacher' }
                    ].map((msg, i) => (
                        <div key={i} className={`flex flex-col ${msg.role === 'teacher' ? 'items-end' : 'items-start'}`}>
                            <span className="text-xs text-slate-400 mb-1">{msg.user}</span>
                            <div className={`px-3 py-2 rounded-xl text-sm max-w-[80%] ${msg.role === 'teacher'
                                    ? 'bg-indigo-600/80 text-white rounded-tr-sm'
                                    : 'bg-slate-700/50 text-slate-200 rounded-tl-sm'
                                }`}>
                                {msg.msg}
                            </div>
                        </div>
                    ))}
                </div>

                <div className="p-4 border-t border-slate-700">
                    <input
                        type="text"
                        placeholder="Type a message..."
                        className="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
                    />
                </div>
            </motion.div>

            <button
                onClick={() => setChatOpen(!chatOpen)}
                className="absolute top-1/2 right-4 w-8 h-16 bg-slate-800/80 backdrop-blur flex items-center justify-center rounded-l-xl border-y border-l border-slate-700 text-slate-400 hover:text-white transition-colors"
            >
                {chatOpen ? '>' : '<'}
            </button>
        </div>
    );
};

export default LiveClassroom;
