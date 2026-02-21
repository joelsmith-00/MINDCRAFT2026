# 🎯 Dot Dev Club Management App - Complete Setup Guide

## 📋 Overview
This is a complete Flutter application for the Dot Dev club featuring:
- ✅ Firebase Authentication (FREE)
- ✅ MongoDB Atlas Database (FREE)
- ✅ Cloudinary File Storage (FREE)
- ✅ Premium UI with Framer Motion-style animations
- ✅ Role-based access (Admin, Team Leader, Member)
- ✅ Attendance tracking
- ✅ Project management
- ✅ Team collaboration

---

## 🚀 Step 1: Install Dependencies

Run this command in the project directory:

```bash
flutter pub get
```

---

## 🔥 Step 2: Firebase Setup

### 2.1 Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project"
3. Name it "DotDev Club" (or your preferred name)
4. Disable Google Analytics (optional)
5. Click "Create Project"

### 2.2 Add Android App
1. In Firebase Console, click the Android icon
2. **Android package name**: `com.dotdev.dotdev_club`
3. Download `google-services.json`
4. Place it in: `android/app/google-services.json`

### 2.3 Add iOS App (if targeting iOS)
1. Click the iOS icon
2. **iOS bundle ID**: `com.dotdev.dotdevClub`
3. Download `GoogleService-Info.plist`
4. Place it in: `ios/Runner/GoogleService-Info.plist`

### 2.4 Enable Email/Password Authentication
1. In Firebase Console → Authentication → Sign-in method
2. Enable "Email/Password"
3. Click "Save"

---

## 🍃 Step 3: MongoDB Atlas Setup (100% FREE)

### 3.1 Create MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for FREE (no credit card required)
3. Create a FREE M0 cluster (512MB storage)

### 3.2 Get Connection String
1. Click "Connect" on your cluster
2. Choose "Connect your application"
3. Copy the connection string (looks like):
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `<username>` and `<password>` with your database credentials

### 3.3 Configure Network Access
1. Go to "Network Access" in MongoDB Atlas
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (for development)
4. Click "Confirm"

### 3.4 Update App Configuration
Open `lib/config/app_config.dart` and update:

```dart
static const String mongoDbUrl = 'YOUR_MONGODB_CONNECTION_STRING_HERE';
```

---

## ☁️ Step 4: Cloudinary Setup (100% FREE)

### 4.1 Create Cloudinary Account
1. Go to [Cloudinary](https://cloudinary.com/users/register/free)
2. Sign up for FREE (no credit card required)
3. Verify your email

### 4.2 Get Credentials
1. Go to Dashboard
2. Note down:
   - **Cloud Name**
   - **API Key**

### 4.3 Create Upload Preset
1. Go to Settings → Upload
2. Scroll to "Upload presets"
3. Click "Add upload preset"
4. **Preset name**: `dotdev_uploads`
5. **Signing Mode**: "Unsigned"
6. **Folder**: `dotdev_club`
7. Click "Save"

### 4.4 Update App Configuration
Open `lib/config/app_config.dart` and update:

```dart
static const String cloudinaryCloudName = 'YOUR_CLOUD_NAME';
static const String cloudinaryApiKey = 'YOUR_API_KEY';
static const String cloudinaryUploadPreset = 'dotdev_uploads';
```

---

## 🎨 Step 5: Add Your Logo

### Option 1: Use Provided Logo
Save your Dot Dev logo image as:
- `assets/images/logo.png`

### Option 2: Generate Logo
The app currently uses a text-based logo. You can:
1. Save your logo image to `assets/images/logo.png`
2. Update the splash screen and login screen to use:
   ```dart
   Image.asset('assets/images/logo.png', width: 150, height: 150)
   ```

---

## 🏃 Step 6: Run the App

### For Android
```bash
flutter run
```

### For iOS (Mac only)
```bash
cd ios
pod install
cd ..
flutter run
```

### For Web
```bash
flutter run -d chrome
```

---

## 👤 Step 7: Create First Admin User

### 7.1 Register First User
1. Run the app
2. Click "Sign Up"
3. Fill in all details
4. Register

### 7.2 Make User an Admin
1. Go to MongoDB Atlas
2. Open your cluster → Browse Collections
3. Find `dotdev_club` database → `users` collection
4. Find your user document
5. Edit the document and change:
   ```json
   "role": "admin"
   ```
6. Save

Now you can log in as an admin!

---

## 📱 App Features

### For Members
- ✅ Register and login
- ✅ Request to join teams
- ✅ Upload projects
- ✅ View attendance
- ✅ Update profile

### For Team Leaders
- ✅ All member features
- ✅ Approve team join requests
- ✅ Mark attendance for team members
- ✅ Review team projects
- ✅ View team analytics

### For Admins
- ✅ All features
- ✅ Create and manage teams
- ✅ Assign team leaders
- ✅ View all members
- ✅ Manage all projects
- ✅ View complete attendance
- ✅ System-wide analytics

---

## 🎬 Animations

The app includes **Framer Motion-style animations**:
- ✨ Fade in/out effects
- ✨ Slide transitions
- ✨ Scale animations
- ✨ Staggered element animations
- ✨ Shimmer loading effects
- ✨ Smooth page transitions

All animations are declarative and use the `flutter_animate` package.

---

## 🔧 Troubleshooting

### MongoDB Connection Issues
- Ensure your IP is whitelisted in Network Access
- Check that your connection string is correct
- Verify database user credentials

### Firebase Auth Issues
- Ensure `google-services.json` is in the correct location
- Check that Email/Password auth is enabled
- Verify package name matches Firebase configuration

### Cloudinary Upload Issues
- Ensure upload preset is set to "Unsigned"
- Check cloud name and API key are correct
- Verify file size is under 10MB

### Animation Issues
- Run `flutter pub get` to ensure all packages are installed
- Clear build cache: `flutter clean && flutter pub get`

---

## 📦 Project Structure

```
lib/
├── config/
│   ├── app_config.dart       # Configuration constants
│   └── app_theme.dart         # Theme and colors
├── models/
│   ├── user_model.dart
│   ├── team_model.dart
│   ├── project_model.dart
│   ├── attendance_model.dart
│   └── team_request_model.dart
├── services/
│   ├── auth_service.dart      # Firebase Auth
│   ├── mongodb_service.dart   # MongoDB operations
│   └── cloudinary_service.dart # File uploads
├── screens/
│   ├── splash_screen.dart
│   ├── auth/
│   │   ├── login_screen.dart
│   │   └── register_screen.dart
│   └── home/
│       └── home_screen.dart
├── utils/
│   └── animation_utils.dart   # Framer Motion-style animations
└── main.dart
```

---

## 🎯 Next Steps

After setup, you can:
1. ✅ Create teams (Admin)
2. ✅ Invite members
3. ✅ Start tracking attendance
4. ✅ Upload projects
5. ✅ Build additional features

---

## 💡 Tips

- **Free Tier Limits**:
  - MongoDB: 512MB storage, shared cluster
  - Cloudinary: 25GB storage, 25GB bandwidth/month
  - Firebase Auth: Unlimited users

- **Security**: 
  - Never commit `google-services.json` to public repos
  - Keep MongoDB connection string private
  - Use environment variables in production

- **Performance**:
  - Optimize images before upload
  - Use pagination for large lists
  - Cache frequently accessed data

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Firebase, MongoDB, and Cloudinary documentation
3. Check Flutter documentation for platform-specific issues

---

## 🎉 You're All Set!

Your Dot Dev Club Management App is ready to use with:
- 🔐 Secure authentication
- 💾 Free cloud database
- 📁 Free file storage
- 🎨 Premium animations
- 📱 Cross-platform support

**Enjoy managing your club! 🚀**
