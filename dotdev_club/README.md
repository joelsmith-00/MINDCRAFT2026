# 🎯 Dot Dev Club Management App

<div align="center">

![Dot Dev Logo](https://img.shields.io/badge/dot-DEV-00D9FF?style=for-the-badge&logo=flutter&logoColor=white)

**A Complete Club Management Solution with 100% Free Cloud Services**

[![Flutter](https://img.shields.io/badge/Flutter-3.38.5-02569B?logo=flutter)](https://flutter.dev)
[![Firebase](https://img.shields.io/badge/Firebase-FREE-FFCA28?logo=firebase)](https://firebase.google.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-FREE-47A248?logo=mongodb)](https://www.mongodb.com/cloud/atlas)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-FREE-3448C5?logo=cloudinary)](https://cloudinary.com)

</div>

---

## ✨ Features

### 🔐 Authentication & Security
- Firebase Authentication (Email/Password)
- Role-based access control (Admin, Team Leader, Member)
- Secure user sessions
- Password reset functionality

### 👥 User Management
- User registration with profile photos
- Complete member profiles (Name, Reg. No., Email, Phone, Role)
- Team assignment and management
- Profile updates

### 🏢 Team Management
- Create and manage multiple teams
- Assign team leaders
- Team join request system
- Member approval workflow
- Team-wise analytics

### 📊 Project Management
- Upload project files (PDF, ZIP)
- GitHub repository integration
- Project review and approval system
- Technology stack tracking
- Feedback mechanism
- File storage via Cloudinary

### 📅 Attendance Tracking
- Daily attendance marking
- Multiple status options (Present, Absent, Late, Leave)
- Individual attendance history
- Team-wise attendance reports
- Attendance percentage calculation
- Date-wise filtering

### 🎨 Premium UI/UX
- **Framer Motion-style animations**
- Dark theme with gradient accents
- Smooth page transitions
- Staggered element animations
- Shimmer loading effects
- Responsive design
- Material Design 3

---

## 🏗️ Architecture

### Tech Stack
- **Frontend**: Flutter (Dart)
- **Authentication**: Firebase Auth
- **Database**: MongoDB Atlas (Free M0 Cluster)
- **File Storage**: Cloudinary (Free Plan)
- **Code Hosting**: GitHub
- **State Management**: Provider
- **Animations**: flutter_animate

### Data Flow
```
User → Firebase Auth → Flutter App → MongoDB Atlas
                              ↓
                        Cloudinary (Files)
```

---

## 🚀 Quick Start

### Prerequisites
- Flutter SDK 3.10.4 or higher
- Android Studio / VS Code
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd dotdev_club
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Configure services** (See [SETUP_GUIDE.md](SETUP_GUIDE.md))
   - Set up Firebase project
   - Create MongoDB Atlas cluster
   - Configure Cloudinary account
   - Update `lib/config/app_config.dart`

4. **Run the app**
   ```bash
   flutter run
   ```

📖 **For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

---

## 📱 Screenshots

### Splash Screen
- Animated logo with gradient
- Smooth fade-in effects
- Auto-navigation based on auth state

### Login & Registration
- Clean, modern UI
- Form validation
- Staggered animations
- Profile photo upload

### Dashboard
- Role-based views
- Quick stats cards
- Recent activity feed
- Navigation bar

---

## 🎬 Animations

The app features **Framer Motion-inspired animations**:

```dart
// Example: Fade in from bottom
Widget.fadeInUp(delay: 200.ms)

// Example: Scale with bounce
Widget.scaleIn(curve: Curves.elasticOut)

// Example: Staggered list items
children.map((item, index) => 
  item.fadeInUp(delay: AnimationUtils.staggerDelay(index))
)
```

### Animation Types
- ✨ Fade In/Out
- ✨ Slide (Up, Down, Left, Right)
- ✨ Scale
- ✨ Rotate
- ✨ Shimmer
- ✨ Blur
- ✨ Stagger

---

## 👥 User Roles

### 🧑‍🎓 Member
- Register and login
- Join teams (request-based)
- Upload projects
- View personal attendance
- Update profile

### 🧑‍✈️ Team Leader
- All member features
- Approve team join requests
- Mark team attendance
- Review team projects
- View team analytics

### 👑 Admin
- All features
- Create and manage teams
- Assign team leaders
- View all members
- Manage all projects
- System-wide analytics
- Approve/reject requests

---

## 💾 Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  uid: String,              // Firebase UID
  email: String,
  name: String,
  registrationNumber: String,
  phoneNumber: String,
  role: String,             // admin, team_leader, member
  teamId: String?,
  profilePhotoUrl: String?,
  createdAt: DateTime,
  updatedAt: DateTime
}
```

### Teams Collection
```javascript
{
  _id: ObjectId,
  name: String,
  description: String,
  leaderId: String,         // User UID
  memberIds: [String],      // Array of User UIDs
  createdAt: DateTime,
  updatedAt: DateTime
}
```

### Projects Collection
```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  userId: String,
  teamId: String,
  technologies: [String],
  fileUrl: String?,         // Cloudinary URL
  githubUrl: String?,
  status: String,           // submitted, approved, needs_correction
  feedback: String?,
  submittedAt: DateTime,
  reviewedAt: DateTime?,
  updatedAt: DateTime
}
```

### Attendance Collection
```javascript
{
  _id: ObjectId,
  userId: String,
  teamId: String,
  date: DateTime,
  status: String,           // present, absent, late, leave
  remarks: String?,
  markedBy: String,         // UID of marker
  createdAt: DateTime
}
```

---

## 🔒 Security

- Firebase Authentication for secure login
- MongoDB connection string kept private
- Cloudinary unsigned uploads (preset-based)
- Role-based access control
- Input validation
- Secure file uploads

---

## 💰 Cost Breakdown

| Service | Plan | Storage | Bandwidth | Cost |
|---------|------|---------|-----------|------|
| Firebase Auth | Free | Unlimited users | - | **$0** |
| MongoDB Atlas | M0 | 512 MB | Shared | **$0** |
| Cloudinary | Free | 25 GB | 25 GB/month | **$0** |
| GitHub | Free | Unlimited repos | - | **$0** |
| **TOTAL** | | | | **$0/month** |

✅ **100% FREE - No Credit Card Required**

---

## 📂 Project Structure

```
lib/
├── config/
│   ├── app_config.dart           # App configuration
│   └── app_theme.dart             # Theme & colors
├── models/
│   ├── user_model.dart
│   ├── team_model.dart
│   ├── project_model.dart
│   ├── attendance_model.dart
│   └── team_request_model.dart
├── services/
│   ├── auth_service.dart          # Firebase Auth
│   ├── mongodb_service.dart       # Database operations
│   └── cloudinary_service.dart    # File uploads
├── screens/
│   ├── splash_screen.dart
│   ├── auth/
│   │   ├── login_screen.dart
│   │   └── register_screen.dart
│   └── home/
│       └── home_screen.dart
├── utils/
│   └── animation_utils.dart       # Animation utilities
└── main.dart
```

---

## 🛠️ Development

### Running Tests
```bash
flutter test
```

### Building for Production

**Android**
```bash
flutter build apk --release
```

**iOS**
```bash
flutter build ios --release
```

**Web**
```bash
flutter build web --release
```

---

## 🐛 Troubleshooting

See [SETUP_GUIDE.md](SETUP_GUIDE.md#-troubleshooting) for common issues and solutions.

---

## 🗺️ Roadmap

- [ ] Push notifications
- [ ] Event management
- [ ] Chat functionality
- [ ] Analytics dashboard
- [ ] Export reports (PDF)
- [ ] Multi-language support
- [ ] Dark/Light theme toggle
- [ ] Offline mode

---

## 📄 License

This project is created for educational purposes for the Dot Dev club.

---

## 🙏 Acknowledgments

- Flutter team for the amazing framework
- Firebase for free authentication
- MongoDB Atlas for free database
- Cloudinary for free file storage
- flutter_animate for animation utilities

---

<div align="center">

**Made with ❤️ for Dot Dev Club**

[![Flutter](https://img.shields.io/badge/Made%20with-Flutter-02569B?logo=flutter)](https://flutter.dev)

</div>
