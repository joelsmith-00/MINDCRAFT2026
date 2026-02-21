# 🎬 App Flow & Animation Timeline

## 📱 Complete User Journey

```
┌─────────────────────────────────────────────────────────────┐
│                     APP LAUNCH                               │
│                         ↓                                    │
│  ╔═══════════════════════════════════════════════════╗      │
│  ║           SPLASH SCREEN (3.5s)                    ║      │
│  ║                                                    ║      │
│  ║  [0ms]    Background circles fade in (staggered)  ║      │
│  ║  [0ms]    Logo scales in with elastic bounce      ║      │
│  ║  [400ms]  "dot" slides from left                  ║      │
│  ║  [600ms]  ".DEV" slides from right                ║      │
│  ║  [1000ms] Shimmer effect on logo                  ║      │
│  ║  [1200ms] "Club Management" fades up              ║      │
│  ║  [1500ms] Loading indicator scales in             ║      │
│  ║  [3500ms] Navigate with fade + slide              ║      │
│  ╚═══════════════════════════════════════════════════╝      │
│                         ↓                                    │
│              Check Authentication                            │
│                    ↙        ↘                                │
│          Not Signed In    Signed In                          │
│                ↓              ↓                               │
│  ╔═══════════════════╗  ╔═══════════════════════╗           │
│  ║  LOGIN SCREEN     ║  ║   HOME SCREEN         ║           │
│  ║                   ║  ║                       ║           │
│  ║  [0ms] Logo       ║  ║  • Dashboard          ║           │
│  ║  [200ms] Welcome  ║  ║  • Teams              ║           │
│  ║  [300ms] Subtitle ║  ║  • Projects           ║           │
│  ║  [400ms] Email    ║  ║  • Attendance         ║           │
│  ║  [500ms] Password ║  ║  • Profile            ║           │
│  ║  [600ms] Button   ║  ║                       ║           │
│  ╚═══════════════════╝  ╚═══════════════════════╝           │
│          ↓                                                   │
│    Sign Up Link                                              │
│          ↓                                                   │
│  ╔═══════════════════════════════════════════════╗          │
│  ║         REGISTRATION SCREEN                   ║          │
│  ║                                                ║          │
│  ║  • Profile photo picker (animated)            ║          │
│  ║  • Full name field                            ║          │
│  ║  • Registration number                        ║          │
│  ║  • Email                                      ║          │
│  ║  • Phone number                               ║          │
│  ║  • Password                                   ║          │
│  ║  • Confirm password                           ║          │
│  ║  • Create Account button                      ║          │
│  ║                                                ║          │
│  ║  All fields animate in with stagger           ║          │
│  ╚═══════════════════════════════════════════════╝          │
│                         ↓                                    │
│              Firebase Auth + MongoDB                         │
│                         ↓                                    │
│  ╔═══════════════════════════════════════════════╗          │
│  ║              HOME SCREEN                      ║          │
│  ║                                                ║          │
│  ║  ┌──────────────────────────────────────┐    ║          │
│  ║  │  DASHBOARD (Role-based)              │    ║          │
│  ║  │  • Welcome card with gradient        │    ║          │
│  ║  │  • Quick stats (animated cards)      │    ║          │
│  ║  │  • Recent activity                   │    ║          │
│  ║  └──────────────────────────────────────┘    ║          │
│  ║                                                ║          │
│  ║  Bottom Navigation:                           ║          │
│  ║  [Dashboard] [Teams] [Projects] [Attendance]  ║          │
│  ║                     [Profile]                 ║          │
│  ╚═══════════════════════════════════════════════╝          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Animation Types Used

### 1. **Fade Animations**
```
Opacity: 0 → 1
Duration: 300ms
Curve: easeOut
```
Used for: Text, cards, images

### 2. **Slide Animations**
```
Position: Offset(0, 0.3) → Offset(0, 0)
Duration: 500ms
Curve: easeOut
```
Used for: Form fields, list items

### 3. **Scale Animations**
```
Scale: 0.8 → 1.0
Duration: 800ms
Curve: elasticOut
```
Used for: Logo, buttons, cards

### 4. **Shimmer Effect**
```
Gradient sweep across element
Duration: 1500ms
Color: white with 30% opacity
```
Used for: Logo highlight, loading states

### 5. **Stagger Effect**
```
Base delay: 100ms
Item delay: baseDelay * (index + 1)
```
Used for: Sequential animations

---

## 🔄 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FLUTTER APP                           │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │  Screens   │  │  Services  │  │   Models   │       │
│  │            │  │            │  │            │       │
│  │ • Splash   │→ │ • Auth     │→ │ • User     │       │
│  │ • Login    │  │ • MongoDB  │  │ • Team     │       │
│  │ • Register │  │ • Cloud.   │  │ • Project  │       │
│  │ • Home     │  │            │  │ • Attend.  │       │
│  └────────────┘  └────────────┘  └────────────┘       │
│         ↓              ↓                                │
└─────────────────────────────────────────────────────────┘
          ↓              ↓
    ┌─────────┐    ┌──────────┐    ┌────────────┐
    │Firebase │    │ MongoDB  │    │ Cloudinary │
    │  Auth   │    │  Atlas   │    │            │
    │         │    │          │    │            │
    │ • Login │    │ • Users  │    │ • Photos   │
    │ • Signup│    │ • Teams  │    │ • Files    │
    │ • Reset │    │ • Proj.  │    │            │
    │         │    │ • Attend.│    │            │
    └─────────┘    └──────────┘    └────────────┘
       FREE           FREE             FREE
```

---

## 👥 Role-Based Features

```
┌──────────────────────────────────────────────────────┐
│                    USER ROLES                         │
├──────────────────────────────────────────────────────┤
│                                                       │
│  🧑‍🎓 MEMBER                                           │
│  ├─ Register & Login                                 │
│  ├─ View Profile                                     │
│  ├─ Request to Join Team                             │
│  ├─ Upload Projects                                  │
│  └─ View Own Attendance                              │
│                                                       │
│  🧑‍✈️ TEAM LEADER (inherits Member)                    │
│  ├─ All Member Features                              │
│  ├─ Approve Team Requests                            │
│  ├─ Mark Team Attendance                             │
│  ├─ Review Team Projects                             │
│  └─ View Team Analytics                              │
│                                                       │
│  👑 ADMIN (inherits all)                              │
│  ├─ All Features                                     │
│  ├─ Create Teams                                     │
│  ├─ Assign Team Leaders                              │
│  ├─ View All Members                                 │
│  ├─ Manage All Projects                              │
│  └─ System Analytics                                 │
│                                                       │
└──────────────────────────────────────────────────────┘
```

---

## 📊 Database Collections

```
MongoDB Atlas - dotdev_club Database
│
├─ users
│  ├─ uid (indexed, unique)
│  ├─ email (indexed, unique)
│  ├─ name
│  ├─ registrationNumber
│  ├─ phoneNumber
│  ├─ role
│  ├─ teamId
│  ├─ profilePhotoUrl
│  └─ timestamps
│
├─ teams
│  ├─ _id
│  ├─ name
│  ├─ description
│  ├─ leaderId
│  ├─ memberIds[]
│  └─ timestamps
│
├─ projects
│  ├─ _id
│  ├─ title
│  ├─ description
│  ├─ userId (indexed)
│  ├─ teamId (indexed)
│  ├─ technologies[]
│  ├─ fileUrl
│  ├─ githubUrl
│  ├─ status
│  ├─ feedback
│  └─ timestamps
│
├─ attendance
│  ├─ _id
│  ├─ userId (indexed)
│  ├─ teamId
│  ├─ date (indexed)
│  ├─ status
│  ├─ remarks
│  ├─ markedBy
│  └─ timestamp
│
└─ team_requests
   ├─ _id
   ├─ userId
   ├─ teamId
   ├─ status
   ├─ message
   ├─ respondedBy
   └─ timestamps
```

---

## 🎯 Animation Timeline Details

### Splash Screen (Total: 3.5s)
```
0ms     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        │ Background Circle 1 (fade + scale)
100ms   │ Background Circle 2 (fade + scale)
200ms   │ Background Circle 3 (fade + scale)
        │
0ms     │ Logo Container (fade + scale)
400ms   │ "dot" text (fade + slideX from left)
600ms   │ ".DEV" text (fade + slideX from right)
1000ms  │ Shimmer effect starts
1200ms  │ Subtitle (fade + slideY from bottom)
1500ms  │ Loading indicator (fade + scale)
2000ms  │ Version text (fade + slideY)
        │
3500ms  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Navigate with fade + slide transition (600ms)
```

### Login Screen
```
0ms     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        │ Logo (fade + scale with elastic bounce)
200ms   │ "Welcome Back!" (fade + slideY)
300ms   │ "Sign in to continue" (fade + slideY)
400ms   │ Email field (fade + slideX from left)
500ms   │ Password field (fade + slideX from right)
600ms   │ Sign In button (fade + scale)
        │
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🎨 Color Scheme

```
Primary Colors:
┌────────────────────────────────────────┐
│ Cyan:    #00D9FF  ████████████         │
│ Purple:  #9D4EDD  ████████████         │
│ Gradient: Cyan → Purple                │
└────────────────────────────────────────┘

Background:
┌────────────────────────────────────────┐
│ Dark:    #0A0E27  ████████████         │
│ Card:    #1A1F3A  ████████████         │
└────────────────────────────────────────┘

Status Colors:
┌────────────────────────────────────────┐
│ Success: #10B981  ████████████ Green   │
│ Error:   #EF4444  ████████████ Red     │
│ Warning: #F59E0B  ████████████ Yellow  │
│ Info:    #3B82F6  ████████████ Blue    │
└────────────────────────────────────────┘
```

---

## 📦 Package Dependencies

```
Core:
├─ flutter (SDK)
├─ cupertino_icons
└─ google_fonts

Authentication:
├─ firebase_core
└─ firebase_auth

Database:
└─ mongo_dart

File Storage:
└─ cloudinary_public

File Handling:
├─ image_picker
└─ file_picker

Animations:
├─ flutter_animate  ← Framer Motion-style
├─ animated_text_kit
├─ lottie
└─ shimmer

State Management:
└─ provider

Utilities:
├─ http
├─ intl
└─ uuid
```

---

<div align="center">

**🎬 Complete App Flow with Framer Motion-style Animations**

**Built with Flutter • Powered by FREE Cloud Services**

</div>
