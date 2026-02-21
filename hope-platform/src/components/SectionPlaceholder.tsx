import React from 'react';
import { Construction } from 'lucide-react';

interface Props {
    title: string;
}

const SectionPlaceholder: React.FC<Props> = ({ title }) => {
    return (
        <div className="glass p-12 flex flex-col items-center justify-center text-center min-h-[60vh]">
            <div className="w-20 h-20 bg-slate-800 rounded-full flex items-center justify-center mb-6 shadow-xl border border-slate-700">
                <Construction size={40} className="text-indigo-400" />
            </div>
            <h2 className="text-3xl font-bold text-white mb-2">{title}</h2>
            <p className="text-slate-400 max-w-md">
                This module is currently being built. Check back later for {title.toLowerCase()} features.
            </p>
        </div>
    );
};

export default SectionPlaceholder;
