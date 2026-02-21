import { createContext, useContext, useEffect, useState } from 'react';
import { supabase } from '../lib/supabaseClient';

const AuthContext = createContext({});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [role, setRole] = useState(null); // 'student' or 'teacher'
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let mounted = true;

        const init = async () => {
            try {
                // Add simple timeout to avoid hanging if Supabase is initializing endlessly
                const sessionPromise = supabase.auth.getSession();
                const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject("Timeout"), 5000));

                const { data: { session }, error } = await Promise.race([sessionPromise, timeoutPromise])
                    .catch(e => ({ data: { session: null }, error: e })); // Fallback on error

                if (error) console.warn("Auth check failed (likely demo mode):", error);

                if (mounted) {
                    setUser(session?.user ?? null);
                    if (session?.user) {
                        await fetchUserRole(session.user);
                    } else {
                        setLoading(false);
                    }
                }
            } catch (err) {
                console.error("Auth Init Error:", err);
                if (mounted) setLoading(false);
            }
        };

        init();

        const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
            if (mounted) {
                setUser(session?.user ?? null);
                if (session?.user) {
                    fetchUserRole(session.user);
                } else {
                    setRole(null);
                    setLoading(false);
                }
            }
        });

        return () => {
            mounted = false;
            subscription.unsubscribe();
        };
    }, []);

    const fetchUserRole = async (currentUser) => {
        try {
            // Priority: Check if it's the specific demo user
            if (currentUser.email.includes('demo')) {
                // Demo logic
                if (currentUser.email.includes('teacher')) {
                    setRole('teacher');
                } else {
                    setRole('student');
                }
                setLoading(false);
                return; // Skip supabase fetch for demo users
            }

            // Real DB check
            const { data, error } = await supabase
                .from('users')
                .select('role')
                .eq('id', currentUser.id)
                .single();

            if (data) {
                setRole(data.role);
            } else {
                // Fallback default
                setRole('student');
            }
        } catch (error) {
            console.error('Error fetching role:', error);
            setRole('student'); // Safe fallback
        } finally {
            setLoading(false);
        }
    };

    const signIn = async (email, password) => {
        // DEMO MODE: Bypass Supabase if using demo credentials
        if (email.includes('demo')) {
            const fakeUser = { id: 'demo-user-123', email: email };
            setUser(fakeUser);
            // Set role based on email content
            if (email.includes('teacher')) {
                setRole('teacher');
            } else {
                setRole('student');
            }
            return { user: fakeUser, session: { user: fakeUser } };
        }

        const { data, error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
        return data;
    };

    const signOut = async () => {
        await supabase.auth.signOut();
        setRole(null);
        setUser(null);
    };

    const value = {
        user,
        role,
        signIn,
        signOut,
        loading
    };

    return (
        <AuthContext.Provider value={value}>
            {loading ? (
                <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
                    <div className="flex flex-col items-center gap-4">
                        <div className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
                        <p className="animate-pulse">Loading Hope Academy...</p>
                    </div>
                </div>
            ) : (
                children
            )}
        </AuthContext.Provider>
    );
};
