import { useEffect, useRef } from 'react';
import io from 'socket.io-client';

const SOCKET_URL = import.meta.env.VITE_SERVER_URL || 'http://localhost:3001';

export const useSocket = () => {
    const socket = useRef();

    useEffect(() => {
        socket.current = io(SOCKET_URL);

        return () => {
            if (socket.current) socket.current.disconnect();
        };
    }, []);

    return socket.current;
};
