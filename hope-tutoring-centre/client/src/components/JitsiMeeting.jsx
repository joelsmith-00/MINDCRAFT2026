import { useEffect, useRef, useState } from 'react';

export default function JitsiMeeting({ roomName, userName, onLeave }) {
    const jitsiContainer = useRef(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Load Jitsi API script
        const script = document.createElement('script');
        script.src = 'https://meet.jit.si/external_api.js';
        script.async = true;
        script.onload = () => {
            setLoading(false);
            initializeMeeting();
        };
        document.body.appendChild(script);

        return () => {
            document.body.removeChild(script);
            // Clean up Jitsi instance if possible
        };
    }, []);

    const initializeMeeting = () => {
        if (!window.JitsiMeetExternalAPI) return;

        const domain = 'meet.jit.si'; // Replace with your self-hosted domain
        const options = {
            roomName: roomName,
            width: '100%',
            height: '100%',
            parentNode: jitsiContainer.current,
            userInfo: {
                displayName: userName
            },
            configOverwrite: {
                startWithAudioMuted: true,
                startWithVideoMuted: true,
            },
            interfaceConfigOverwrite: {
                SHOW_JITSI_WATERMARK: false,
            }
        };

        const api = new window.JitsiMeetExternalAPI(domain, options);

        api.addEventListeners({
            videoConferenceLeft: () => {
                if (onLeave) onLeave();
            },
        });
    };

    return (
        <div className="w-full h-full relative bg-black rounded-2xl overflow-hidden glass-card">
            {loading && (
                <div className="absolute inset-0 flex items-center justify-center text-white">
                    Loading Meeting...
                </div>
            )}
            <div ref={jitsiContainer} className="w-full h-full" />
        </div>
    );
}
