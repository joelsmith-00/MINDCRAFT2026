import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useSocket } from '../hooks/useSocket';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, XCircle, Send, Plus } from 'lucide-react';

export default function MCQPanel({ meetingId }) {
    const { role } = useAuth(); // 'student' or 'teacher'
    const socket = useSocket();
    const [activeTest, setActiveTest] = useState(null);
    const [studentAnswers, setStudentAnswers] = useState({});
    const [testResults, setTestResults] = useState([]); // For teacher

    // Teacher State: Creating Test
    const [newQuestion, setNewQuestion] = useState({ text: '', options: ['', '', '', ''], correct: 0 });

    useEffect(() => {
        if (!socket) return;

        // Listen for incoming tests (Student)
        socket.on('receive_test', (test) => {
            console.log("Received test", test);
            setActiveTest(test);
        });

        // Listen for incoming answers (Teacher)
        socket.on('student_submitted', (data) => {
            setTestResults(prev => [...prev, data]);
        });

        return () => {
            socket.off('receive_test');
            socket.off('student_submitted');
        };
    }, [socket]);

    const startTest = () => {
        if (!newQuestion.text) return;
        const testData = {
            id: Date.now(),
            question: newQuestion.text,
            options: newQuestion.options,
            correct: newQuestion.correct
        };
        // Emit to server
        socket.emit('start_test', { meetingId, testData });
        setActiveTest(testData); // Show to teacher too just for confirmation
    };

    const submitAnswer = (optionIndex) => {
        const isCorrect = optionIndex === activeTest.correct;
        socket.emit('submit_answer', { meetingId, studentId: 'me', correct: isCorrect });
        setActiveTest(null); // Clear test after submitting
        alert(isCorrect ? "Correct!" : "Wrong answer!");
    };

    if (!activeTest && role === 'student') {
        return (
            <div className="p-4 text-center text-slate-400">
                Waiting for teacher to start a test...
            </div>
        )
    }

    if (role === 'teacher') {
        return (
            <div className="bg-slate-800 p-4 rounded-xl">
                <h3 className="text-lg font-bold mb-4 text-white">Live MCQ Panel</h3>

                {!activeTest ? (
                    <div className="space-y-4">
                        <input
                            className="w-full bg-slate-700 border-slate-600 rounded p-2 text-white"
                            placeholder="Question Text"
                            value={newQuestion.text}
                            onChange={e => setNewQuestion({ ...newQuestion, text: e.target.value })}
                        />
                        <div className="grid grid-cols-2 gap-2">
                            {newQuestion.options.map((opt, i) => (
                                <div key={i} className="flex gap-2">
                                    <input
                                        type="radio"
                                        name="correct"
                                        checked={newQuestion.correct === i}
                                        onChange={() => setNewQuestion({ ...newQuestion, correct: i })}
                                    />
                                    <input
                                        className="w-full bg-slate-700 border-slate-600 rounded p-2 text-white text-sm"
                                        placeholder={`Option ${i + 1}`}
                                        value={opt}
                                        onChange={e => {
                                            const newOpts = [...newQuestion.options];
                                            newOpts[i] = e.target.value;
                                            setNewQuestion({ ...newQuestion, options: newOpts });
                                        }}
                                    />
                                </div>
                            ))}
                        </div>
                        <button
                            onClick={startTest}
                            className="w-full bg-primary-600 hover:bg-primary-500 text-white py-2 rounded-lg flex items-center justify-center gap-2"
                        >
                            <Send size={16} /> Broadcast Test
                        </button>
                    </div>
                ) : (
                    <div>
                        <p className="text-green-400 mb-2">Test Live: {activeTest.question}</p>
                        <button onClick={() => setActiveTest(null)} className="text-sm text-red-400 underline">End Test</button>
                        <div className="mt-4">
                            <h4 className="font-bold text-white mb-2">Live Results:</h4>
                            {testResults.length === 0 && <p className="text-slate-500 text-sm">Waiting for answers...</p>}
                            <div className="flex gap-2 flex-wrap">
                                {testResults.map((res, i) => (
                                    <span key={i} className={`px-2 py-1 rounded text-xs ${res.correct ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                                        {res.correct ? 'Correct' : 'Wrong'}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        );
    }

    return (
        <div className="bg-slate-800 p-6 rounded-xl shadow-xl border border-primary-500/20">
            <h3 className="text-xl font-bold mb-4 text-white">Pop Quiz!</h3>
            <p className="text-lg mb-6 text-white">{activeTest.question}</p>

            <div className="space-y-3">
                {activeTest.options.map((opt, i) => (
                    <motion.button
                        key={i}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => submitAnswer(i)}
                        className="w-full text-left p-4 rounded-lg bg-slate-700 hover:bg-primary-600 transition-colors text-white font-medium"
                    >
                        {opt}
                    </motion.button>
                ))}
            </div>
        </div>
    );
}
