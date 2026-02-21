# 🚀 DOTDEV Club App - Quick Reference

## ⚡ Quick Start (3 Steps)

### 1️⃣ Firebase Setup
```bash
# Go to: https://console.firebase.google.com/
# Create project: "dotdev-club"
# Enable: Authentication (Email/Password)
# Enable: Firestore Database
# Enable: Cloud Storage
# Download: google-services.json → android/app/
```

### 2️⃣ Update Config
```dart
// In lib/main.dart, replace:
apiKey: 'YOUR_API_KEY',
appId: 'YOUR_APP_ID',
messagingSenderId: 'YOUR_SENDER_ID',
projectId: 'dotdev-club',
storageBucket: 'dotdev-club.appspot.com',
```

### 3️⃣ Run App
```bash
cd dotdev_club
flutter run
```

---

## 📱 App Features at a Glance

| Feature | Admin | Team Leader | Member |
|---------|-------|-------------|--------|
| View Dashboard | ✅ | ✅ | ✅ |
| Track Attendance | ✅ | ✅ | ✅ |
| Upload Projects | ✅ | ✅ | ✅ |
| Create Teams | ✅ | ✅ | ❌ |
| Approve Requests | ✅ | ✅ | ❌ |
| View All Users | ✅ | ❌ | ❌ |
| View All Projects | ✅ | ❌ | ❌ |
| Manage Attendance | ✅ | ✅ | ❌ |

---

## 🎨 Color Palette

```dart
Primary:    #6C63FF  // Purple
Secondary:  #00D9FF  // Cyan
Accent:     #FF6584  // Pink
Dark BG:    #0F0F1E  // Deep Navy
Card BG:    #1A1A2E  // Dark Blue
Surface:    #16213E  // Blue Gray
```

---

## 📂 File Structure

```
lib/
├── models/          → Data structures
├── services/        → Firebase logic
├── providers/       → State management
├── screens/         → UI pages
├── utils/           → Theme & helpers
└── main.dart        → Entry point
```

---

## 🔑 Key Commands

```bash
# Get dependencies
flutter pub get

# Clean build
flutter clean

# Run app
flutter run

# Build APK
flutter build apk

# Check for issues
flutter doctor
```

---

## 👤 User Workflows

### New Member:
1. Sign up → Select "Member"
2. Browse teams → Request to join
3. Wait for approval
4. Upload projects
5. View attendance

### Team Leader:
1. Sign up → Select "Team Leader"
2. Create team
3. Approve join requests
4. Manage team members
5. Track team progress

### Admin:
1. Sign up (first user = admin)
2. Access admin dashboard
3. View all users/projects
4. Manage attendance
5. Oversee entire club

---

## 🔐 Firebase Security Rules

### Firestore (Basic):
```javascript
match /{document=**} {
  allow read, write: if request.auth != null;
}
```

### Storage (Basic):
```javascript
match /{allPaths=**} {
  allow read, write: if request.auth != null;
}
```

---

## 🐛 Quick Fixes

### Build Error?
```bash
flutter clean && flutter pub get
```

### Firebase Error?
- Check `google-services.json` location
- Verify Firebase config in `main.dart`
- Enable required services in console

### Upload Not Working?
- Check internet connection
- Verify Storage is enabled
- Check storage rules

---

## 📊 Screen Navigation

```
Login
  ↓
Home (Dashboard)
  ├→ Attendance
  ├→ Projects
  ├→ Team
  ├→ Admin (Admin only)
  └→ Profile
```

---

## 💾 Data Models

**User:** uid, email, name, role, teamId, isApproved
**Project:** id, title, description, userId, fileUrls, imageUrls
**Attendance:** id, userId, sessionTitle, isPresent, sessionDate
**Team:** id, name, leaderId, memberIds
**JoinRequest:** id, userId, teamId, status

---

## 🎯 Important Notes

⚠️ **First user should sign up as Admin**
⚠️ **Update Firebase config before running**
⚠️ **Enable all Firebase services**
⚠️ **Team Leaders must create teams first**
⚠️ **Members need approval to join teams**

---

## 📚 Documentation Files

- `README.md` - Full documentation
- `FEATURES.md` - Feature details
- `FIREBASE_SETUP.md` - Firebase guide
- `PROJECT_SUMMARY.md` - Complete overview
- `QUICK_REFERENCE.md` - This file

---

## 🎨 Customization

### Change Colors:
Edit `lib/utils/theme.dart`

### Change Font:
```dart
GoogleFonts.robotoTextTheme()  // Instead of poppins
```

### Add Features:
Build on existing models and services

---

## 📞 Help Resources

- Flutter Docs: https://docs.flutter.dev/
- Firebase Docs: https://firebase.google.com/docs
- FlutterFire: https://firebase.flutter.dev/

---

## ✅ Pre-Launch Checklist

- [ ] Firebase project created
- [ ] Authentication enabled
- [ ] Firestore enabled
- [ ] Storage enabled
- [ ] google-services.json added
- [ ] Firebase config updated in main.dart
- [ ] Dependencies installed
- [ ] App runs successfully
- [ ] Admin account created
- [ ] Test all features

---

**🎉 You're Ready to Launch!**

**DOTDEV Club Management App v1.0.0**
