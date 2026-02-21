import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { PageTransition } from './PageTransition';

export const ProtectedRoute = ({ allowedRoles }) => {
    const { user, role } = useAuth();

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (allowedRoles && !allowedRoles.includes(role)) {
        // Redirect to their appropriate dashboard if they try to access wrong area
        return <Navigate to={role === 'teacher' ? '/teacher-dashboard' : '/student-dashboard'} replace />;
    }

    return (
        <PageTransition>
            <Outlet />
        </PageTransition>
    );
};
