const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "http://localhost:5173", // Allow vite client
    methods: ["GET", "POST"]
  }
});

// Socket.io connection handling
io.on('connection', (socket) => {
  console.log(`User connected: ${socket.id}`);

  socket.on('join_meeting', (data) => {
    socket.join(data.meetingId);
    console.log(`User ${socket.id} joined meeting ${data.meetingId}`);
  });

  socket.on('start_test', (data) => {
    // Broadcast test to all students in the room
    socket.to(data.meetingId).emit('receive_test', data.testData);
  });

  socket.on('submit_answer', (data) => {
    // Send answer to teacher
    // In a real app, verify teacher's socket ID or broadcast to room with teacher role
    // For now, simpler implementation
    io.emit('student_submitted', data); 
  });

  socket.on('disconnect', () => {
    console.log('User disconnected', socket.id);
  });
});

const PORT = process.env.PORT || 3001;

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
