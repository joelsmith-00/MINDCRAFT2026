# Firebase Setup Guide for DOTDEV Club App

## Quick Start (5 Minutes)

### Step 1: Create Firebase Project
1. Go to https://console.firebase.google.com/
2. Click "Add project"
3. Enter project name: **dotdev-club**
4. Disable Google Analytics (optional)
5. Click "Create project"

### Step 2: Register Your App

#### For Android:
1. Click the Android icon
2. Enter package name: `com.dotdev.dotdev_club`
3. Download `google-services.json`
4. Place it in: `android/app/google-services.json`

#### For iOS (Optional):
1. Click the iOS icon
2. Enter bundle ID: `com.dotdev.dotdevClub`
3. Download `GoogleService-Info.plist`
4. Place it in: `ios/Runner/GoogleService-Info.plist`

### Step 3: Enable Authentication
1. In Firebase Console, go to **Authentication**
2. Click "Get started"
3. Click "Sign-in method" tab
4. Enable **Email/Password**
5. Click "Save"

### Step 4: Create Firestore Database
1. In Firebase Console, go to **Firestore Database**
2. Click "Create database"
3. Select **Start in production mode**
4. Choose location (closest to you)
5. Click "Enable"

### Step 5: Update Security Rules

#### Firestore Rules:
1. Go to Firestore Database > Rules
2. Replace with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow authenticated users to read/write their own data
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

3. Click "Publish"

### Step 6: Enable Cloud Storage
1. In Firebase Console, go to **Storage**
2. Click "Get started"
3. Start in **production mode**
4. Click "Done"

#### Storage Rules:
1. Go to Storage > Rules
2. Replace with:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

3. Click "Publish"

### Step 7: Get Firebase Configuration

1. Go to Project Settings (gear icon)
2. Scroll down to "Your apps"
3. Find your app and look for "SDK setup and configuration"
4. Copy the configuration values

### Step 8: Update main.dart

Open `lib/main.dart` and replace the Firebase options:

```dart
await Firebase.initializeApp(
  options: const FirebaseOptions(
    apiKey: 'YOUR_API_KEY_HERE',
    appId: 'YOUR_APP_ID_HERE',
    messagingSenderId: 'YOUR_SENDER_ID_HERE',
    projectId: 'dotdev-club',
    storageBucket: 'dotdev-club.appspot.com',
  ),
);
```

**Where to find these values:**
- **apiKey**: In Firebase Console > Project Settings > General > Web API Key
- **appId**: In Firebase Console > Project Settings > Your apps > App ID
- **messagingSenderId**: In Firebase Console > Project Settings > Cloud Messaging > Sender ID
- **projectId**: Your project ID (e.g., "dotdev-club")
- **storageBucket**: Usually `[projectId].appspot.com`

### Step 9: Android Configuration

1. Open `android/build.gradle`
2. Add this to dependencies (if not already there):
```gradle
classpath 'com.google.gms:google-services:4.3.15'
```

3. Open `android/app/build.gradle`
4. Add this at the bottom (if not already there):
```gradle
apply plugin: 'com.google.gms.google-services'
```

### Step 10: Run the App!

```bash
cd dotdev_club
flutter run
```

---

## Production-Ready Security Rules (Optional)

### Firestore Rules (Advanced):

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Helper function to check if user is admin
    function isAdmin() {
      return get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
    
    // Helper function to check if user is team leader
    function isTeamLeader() {
      return get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'teamLeader';
    }
    
    // Users collection
    match /users/{userId} {
      allow read: if request.auth != null;
      allow create: if request.auth.uid == userId;
      allow update: if request.auth.uid == userId || isAdmin();
      allow delete: if isAdmin();
    }
    
    // Teams collection
    match /teams/{teamId} {
      allow read: if request.auth != null;
      allow create: if request.auth != null && isTeamLeader();
      allow update: if resource.data.leaderId == request.auth.uid || isAdmin();
      allow delete: if isAdmin();
    }
    
    // Projects collection
    match /projects/{projectId} {
      allow read: if request.auth != null;
      allow create: if request.auth != null;
      allow update: if resource.data.userId == request.auth.uid || isAdmin();
      allow delete: if resource.data.userId == request.auth.uid || isAdmin();
    }
    
    // Attendance collection
    match /attendance/{attendanceId} {
      allow read: if request.auth != null;
      allow create: if isTeamLeader() || isAdmin();
      allow update: if isAdmin();
      allow delete: if isAdmin();
    }
    
    // Join Requests collection
    match /joinRequests/{requestId} {
      allow read: if request.auth != null;
      allow create: if request.auth != null;
      allow update: if resource.data.teamLeaderId == request.auth.uid || isAdmin();
      allow delete: if isAdmin();
    }
  }
}
```

### Storage Rules (Advanced):

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Projects folder
    match /projects/{userId}/{allPaths=**} {
      allow read: if request.auth != null;
      allow write: if request.auth.uid == userId;
      allow delete: if request.auth.uid == userId;
    }
    
    // Profile pictures
    match /profiles/{userId}/{allPaths=**} {
      allow read: if request.auth != null;
      allow write: if request.auth.uid == userId;
    }
  }
}
```

---

## Troubleshooting

### Issue: "No Firebase App has been created"
**Solution:** Make sure you've added the Firebase initialization code in `main.dart` before `runApp()`.

### Issue: "google-services.json not found"
**Solution:** 
1. Download the file from Firebase Console
2. Place it exactly at: `android/app/google-services.json`
3. Run `flutter clean` and `flutter pub get`

### Issue: "Permission denied" errors
**Solution:** Update your Firestore and Storage security rules as shown above.

### Issue: "Platform exception" on file upload
**Solution:** 
1. Check that Storage is enabled in Firebase Console
2. Verify storage rules allow authenticated writes
3. Ensure you have internet connection

### Issue: Build fails on Windows
**Solution:** 
1. Enable Developer Mode: `start ms-settings:developers`
2. Or ignore the warning - it's optional for development

---

## Testing Your Setup

### Test 1: Authentication
1. Run the app
2. Sign up with a test email
3. Check Firebase Console > Authentication > Users
4. You should see your new user

### Test 2: Firestore
1. After signup, check Firestore Database
2. You should see a `users` collection
3. With a document containing your user data

### Test 3: Storage (After uploading a project)
1. Upload a project with files
2. Check Storage in Firebase Console
3. You should see files in `projects/[userId]/` folder

---

## Next Steps

1. ✅ Complete Firebase setup
2. ✅ Run the app
3. ✅ Create admin account (first signup)
4. ✅ Test all features
5. 🎨 Customize colors in `lib/utils/theme.dart`
6. 📱 Build for production: `flutter build apk`

---

## Support

If you encounter issues:
1. Check the [README.md](README.md) for general setup
2. Review [FEATURES.md](FEATURES.md) for feature documentation
3. Verify all Firebase services are enabled
4. Check Firebase Console for error logs

---

**Happy Coding! 🚀**
**DOTDEV Club**
