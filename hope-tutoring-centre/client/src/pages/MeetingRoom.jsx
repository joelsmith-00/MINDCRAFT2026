import { useParams, useNavigate } from 'react-router-dom';
import JitsiMeeting from '../components/JitsiMeeting';
import MCQPanel from '../components/MCQPanel';
import { useAuth } from '../context/AuthContext';
import { useState } from 'react';

export default function MeetingRoom() {
    const { meetingId } = useParams();
    const { user, role } = useAuth();
    const navigate = useNavigate();
    const [showMCQ, setShowMCQ] = useState(true);

    const handleLeave = () => {
        navigate(role === 'teacher' ? '/teacher-dashboard' : '/student-dashboard');
    };

    return (
        <div className="h-screen w-screen bg-black flex flex-col md:flex-row overflow-hidden">
            {/* Main Video Area */}
            <div className="flex-1 relative h-full">
                <JitsiMeeting
                    roomName={meetingId || 'hope-tuting-centre-main'}
                    userName={user?.email || 'Guest'}
                    onLeave={handleLeave}
                />
            </div>

            {/* Sidebar (Chat / MCQ) */}
            <div className="w-full md:w-96 bg-slate-900 border-l border-slate-800 flex flex-col h-1/2 md:h-full">
                <div className="flex border-b border-slate-800">
                    <button
                        onClick={() => setShowMCQ(false)}
                        className={`flex-1 p-3 font-medium ${!showMCQ ? 'text-primary-400 border-b-2 border-primary-400' : 'text-slate-400'}`}
                    >
                        Chat
                    </button>
                    <button
                        onClick={() => setShowMCQ(true)}
                        className={`flex-1 p-3 font-medium ${showMCQ ? 'text-primary-400 border-b-2 border-primary-400' : 'text-slate-400'}`}
                    >
                        MCQ / Tests
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-4">
                    {showMCQ ? (
                        <MCQPanel meetingId={meetingId || 'hope-tuting-centre-main'} />
                    ) : (
                        <div className="text-center text-slate-500 mt-10">
                            <p>Chat is handled inside Jitsi.</p>
                            <p className="text-xs mt-2">Use the video interface chat button.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
