import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';

export const CountUp = ({ to, duration = 2 }) => {
    // Simplified count up for demo, can rely on pure CSS or framer motion useTransform for advanced
    // For now, pure React state approach is fine for 0-100
    const [count, setCount] = useState(0);

    // In a real premium app, use 'useSpring' from framer-motion

    return (
        <motion.span
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            onViewportEnter={() => {
                let start = 0;
                const end = parseInt(to.toString(), 10);
                if (start === end) return;
                const totalMilSec = duration * 1000;
                const incrementTime = (totalMilSec / end);

                let timer = setInterval(() => {
                    start += 1;
                    setCount(start);
                    if (start >= end) clearInterval(timer);
                }, incrementTime);
            }}
        >
            {count}
        </motion.span>
    )
}

export const GlassCard = ({ children, className = "", delay = 0 }) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay, ease: "easeOut" }}
        className={`glass-card p-6 rounded-2xl relative overflow-hidden group hover:shadow-primary-500/10 hover:border-primary-500/30 transition-all duration-300 ${className}`}
    >
        <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
        <div className="relative z-10">{children}</div>
    </motion.div>
);
