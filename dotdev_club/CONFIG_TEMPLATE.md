# 🔧 Configuration Template

## Copy this file and fill in your credentials

---

## 🍃 MongoDB Atlas Configuration

**Connection String:**
```
mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

**How to get it:**
1. Go to MongoDB Atlas Dashboard
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string
5. Replace <username> and <password> with your database credentials

**Database Name:** `dotdev_club`

---

## ☁️ Cloudinary Configuration

**Cloud Name:** `_________________`

**API Key:** `_________________`

**Upload Preset:** `dotdev_uploads`

**How to get it:**
1. Go to Cloudinary Dashboard
2. Find Cloud Name and API Key in the dashboard
3. Create an upload preset:
   - Settings → Upload → Add upload preset
   - Name: `dotdev_uploads`
   - Signing Mode: Unsigned
   - Folder: `dotdev_club`

---

## 🔥 Firebase Configuration

### Android
1. Download `google-services.json` from Firebase Console
2. Place it in: `android/app/google-services.json`

### iOS
1. Download `GoogleService-Info.plist` from Firebase Console
2. Place it in: `ios/Runner/GoogleService-Info.plist`

### Enable Authentication
1. Firebase Console → Authentication
2. Sign-in method → Email/Password
3. Enable and Save

---

## 📝 Update app_config.dart

After getting your credentials, update `lib/config/app_config.dart`:

```dart
class AppConfig {
  // MongoDB Atlas Configuration
  static const String mongoDbUrl = 'YOUR_MONGODB_CONNECTION_STRING';
  static const String databaseName = 'dotdev_club';
  
  // Cloudinary Configuration
  static const String cloudinaryCloudName = 'YOUR_CLOUD_NAME';
  static const String cloudinaryApiKey = 'YOUR_API_KEY';
  static const String cloudinaryUploadPreset = 'dotdev_uploads';
  
  // ... rest of the config
}
```

---

## ✅ Verification Checklist

- [ ] MongoDB Atlas cluster created (M0 Free tier)
- [ ] MongoDB connection string obtained
- [ ] MongoDB Network Access configured (Allow from anywhere for dev)
- [ ] Cloudinary account created
- [ ] Cloudinary cloud name and API key obtained
- [ ] Cloudinary upload preset created (unsigned)
- [ ] Firebase project created
- [ ] Firebase Email/Password auth enabled
- [ ] google-services.json downloaded and placed
- [ ] app_config.dart updated with all credentials
- [ ] flutter pub get executed successfully

---

## 🎯 Quick Test

After configuration:

1. Run the app: `flutter run`
2. Register a new user
3. Check MongoDB Atlas → Browse Collections → users (should see new user)
4. Upload a profile photo during registration
5. Check Cloudinary → Media Library (should see uploaded photo)
6. Login with the registered user
7. Success! 🎉

---

## 🆘 Need Help?

See SETUP_GUIDE.md for detailed instructions and troubleshooting.
