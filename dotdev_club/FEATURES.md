# DOTDEV Club App - Feature Overview

## 🎨 App Screens & Features

### 1. **Login/Signup Screen**
- **Premium animated login interface**
- Gradient background with floating animations
- Role selection (Admin, Team Leader, Member)
- Email/Password authentication
- Smooth fade-in animations
- Toggle between login and signup

**Features:**
- Form validation
- Error handling with snackbars
- Auto-navigation after successful login
- Beautiful gradient logo with DOTDEV branding

---

### 2. **Dashboard (Home Screen)**
- **Personalized welcome card** with gradient background
- **Role badge** showing user's current role
- **Quick stats cards** displaying:
  - Attendance percentage
  - Total projects
  - Team name
  - Total sessions attended
- **Recent activity feed** showing latest actions
- **Bottom navigation** with role-based menu items

**Navigation Items:**
- Dashboard (All users)
- Attendance (All users)
- Projects (All users)
- Team (Team Leaders & Members)
- Admin (Admin only)
- Profile (All users)

---

### 3. **Attendance Screen**
- **Statistics card** with gradient showing:
  - Overall attendance percentage
  - Total sessions
  - Attended sessions
  - Missed sessions
- **Session history list** with:
  - Session title
  - Date
  - Present/Absent status
  - Color-coded indicators

**Features:**
- Real-time attendance tracking
- Automatic percentage calculation
- Beautiful card-based UI
- Empty state with helpful message

---

### 4. **Projects Screen**
- **Project upload functionality**
- **Multi-file and image upload**
- **Project cards** displaying:
  - Project title
  - Description
  - Author name
  - Upload date
  - File count
  - Image count
- **Gradient headers** on project cards

**Upload Dialog Features:**
- Title and description input
- Image picker (multiple images)
- File picker (multiple files)
- Upload progress indicator
- Success confirmation

---

### 5. **Team Screen**

#### For Team Leaders:
- **Create team** functionality
- **View team members** with:
  - Member avatars
  - Names and emails
  - Role badges
- **Join request management**
  - Approve/Reject buttons
  - Real-time request updates
  - Notification on approval

#### For Members:
- **Browse available teams**
- **Team information cards** showing:
  - Team name
  - Leader name
  - Member count
  - Description
- **Request to join** functionality
- **View current team** once approved

---

### 6. **Admin Dashboard**
- **Tabbed interface** with three sections:

#### Users Tab:
- **Grouped by role:**
  - Admins (Red accent)
  - Team Leaders (Purple accent)
  - Members (Cyan accent)
- **User cards** showing:
  - Profile avatar
  - Name and email
  - Team affiliation
  - Approval status

#### Projects Tab:
- **All projects** across all teams
- Project details with file/image counts
- Author information
- Quick overview of all submissions

#### Attendance Tab:
- **Mark attendance** for sessions
- **Session overview** showing:
  - Session title
  - Present/Total ratio
  - Session grouping
- **Create new sessions**

---

### 7. **Profile Screen**
- **Large profile header** with gradient
- **User information:**
  - Profile avatar (initial-based)
  - Full name
  - Email
  - Role badge
- **Info cards** displaying:
  - Team membership
  - Member since date
  - Approval status
- **Settings menu:**
  - Edit Profile
  - Notifications
  - Privacy
  - Help & Support
- **DOTDEV branding card** at bottom

---

## 🎨 Design System

### Color Palette:
```
Primary: #6C63FF (Purple)
Secondary: #00D9FF (Cyan)
Accent: #FF6584 (Pink)
Dark Background: #0F0F1E
Card Background: #1A1A2E
Surface Background: #16213E
```

### Typography:
- **Font Family:** Poppins (Google Fonts)
- **Headings:** Bold, 20-28px
- **Body:** Regular, 14-16px
- **Labels:** Medium, 12-14px

### UI Elements:
- **Cards:** Rounded corners (16-24px), subtle shadows
- **Buttons:** Elevated with gradient shadows
- **Inputs:** Filled style with rounded borders
- **Icons:** Material Design icons
- **Gradients:** Linear gradients throughout

---

## 🔐 Security Features

### Authentication:
- Firebase Authentication
- Email/Password login
- Secure password storage
- Session management

### Authorization:
- Role-based access control
- Firestore security rules
- Protected routes
- Data validation

### Data Protection:
- Encrypted storage
- Secure file uploads
- User data privacy
- Team-based data isolation

---

## 📱 User Workflows

### New Member Journey:
1. Sign up with email/password
2. Select "Member" role
3. Browse available teams
4. Request to join a team
5. Wait for TL approval
6. Start uploading projects
7. View attendance records

### Team Leader Journey:
1. Sign up with email/password
2. Select "Team Leader" role
3. Create a team
4. Manage join requests
5. View team members
6. Monitor team projects
7. Track team attendance

### Admin Journey:
1. Sign up as first user (Admin)
2. Access admin dashboard
3. View all users by role
4. Monitor all projects
5. Manage attendance sessions
6. Oversee entire club

---

## 🚀 Technical Highlights

### State Management:
- Provider pattern
- Reactive UI updates
- Efficient rebuilds

### Database:
- Firestore real-time database
- Stream-based data fetching
- Automatic synchronization

### Storage:
- Firebase Cloud Storage
- Secure file uploads
- Download URL generation

### Performance:
- Lazy loading
- Pagination ready
- Optimized queries
- Cached data

---

## 📊 Data Models

### User Model:
- uid, email, name, photoUrl
- role (admin/teamLeader/member)
- teamId, teamName, teamLeaderId
- isApproved, createdAt
- personalInfo (flexible)

### Project Model:
- id, title, description
- userId, userName, teamId
- fileUrls[], imageUrls[]
- createdAt, updatedAt
- metadata (flexible)

### Attendance Model:
- id, userId, userName, teamId
- sessionDate, sessionTitle
- isPresent, markedBy, markedAt

### Team Model:
- id, name, description
- leaderId, leaderName
- memberIds[]
- createdAt

### Join Request Model:
- id, userId, userName
- teamId, teamName, teamLeaderId
- requestedAt, status

---

## 🎯 Key Features Summary

✅ Role-based access (Admin, TL, Member)
✅ Team creation and management
✅ Join request approval system
✅ Project upload with files/images
✅ Attendance tracking with statistics
✅ Real-time data synchronization
✅ Premium dark theme UI
✅ Smooth animations
✅ Responsive design
✅ Secure authentication
✅ Cloud storage integration
✅ Admin dashboard
✅ User profiles
✅ Team collaboration

---

**Built with Flutter & Firebase**
**Designed for DOTDEV Club**
