export type Role = 'student' | 'teacher' | 'admin';

export interface User {
  id: string;
  name: string;
  email: string;
  role: Role;
  avatar?: string;
}

export interface ClassSession {
  id: string;
  title: string;
  subject: string;
  teacherId: string;
  teacherName: string;
  startTime: string; // ISO string
  duration: number; // minutes
  isLive: boolean;
  thumbnail: string;
}

export interface Assignment {
  id: string;
  title: string;
  subject: string;
  dueDate: string;
  status: 'pending' | 'submitted' | 'graded';
  grade?: number;
}

export interface Test {
  id: string;
  title: string;
  subject: string;
  date: string;
  duration: number; // minutes
  totalQuestions: number;
  score?: number;
}
