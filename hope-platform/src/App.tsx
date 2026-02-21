import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import StudentDashboard from './pages/student/Dashboard';
import TeacherDashboard from './pages/teacher/Dashboard';
import AdminDashboard from './pages/admin/Dashboard';
import LiveClassroom from './pages/LiveClassroom';
import SectionPlaceholder from './components/SectionPlaceholder';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />

          <Route element={<Layout />}>
            {/* Common Routes */}
            <Route path="/classroom/:id" element={<LiveClassroom />} />

            {/* Student Routes */}
            <Route element={<ProtectedRoute allowedRoles={['student']} />}>
              <Route path="/student/dashboard" element={<StudentDashboard />} />
              <Route path="/student/classes" element={<StudentDashboard />} />
              <Route path="/student/assignments" element={<SectionPlaceholder title="Assignments" />} />
              <Route path="/student/tests" element={<SectionPlaceholder title="Online Tests" />} />
              <Route path="/student/performance" element={<SectionPlaceholder title="Performance Analytics" />} />
            </Route>

            {/* Teacher Routes */}
            <Route element={<ProtectedRoute allowedRoles={['teacher']} />}>
              <Route path="/teacher/dashboard" element={<TeacherDashboard />} />
              <Route path="/teacher/classes" element={<SectionPlaceholder title="My Classes" />} />
              <Route path="/teacher/assignments" element={<SectionPlaceholder title="Manage Assignments" />} />
              <Route path="/teacher/students" element={<SectionPlaceholder title="Student List" />} />
              <Route path="/teacher/reports" element={<SectionPlaceholder title="Reports & Analytics" />} />
            </Route>

            {/* Admin Routes */}
            <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
              <Route path="/admin/dashboard" element={<AdminDashboard />} />
              <Route path="/admin/users" element={<SectionPlaceholder title="User Management" />} />
              <Route path="/admin/settings" element={<SectionPlaceholder title="Platform Settings" />} />
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
