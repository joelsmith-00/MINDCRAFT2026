# MongoDB Atlas Quick Setup

## 🚀 5-Minute Setup

### 1. MongoDB Atlas Account
1. Visit: https://www.mongodb.com/cloud/atlas/register
2. Sign up (free tier available)
3. Create cluster (M0 Free tier)
4. Wait 3-5 minutes for cluster creation

### 2. Database User
```
Database Access → Add New User
- Username: dotdev_admin
- Password: [Generate secure password]
- Role: Atlas Admin
```

### 3. Network Access
```
Network Access → Add IP Address
- Allow Access from Anywhere (0.0.0.0/0)
- For production: Use specific IPs
```

### 4. Get Connection String
```
Database → Connect → Connect your application
- Driver: Dart
- Copy connection string
- Replace <password> with your actual password
```

Example:
```
mongodb+srv://dotdev_admin:YOUR_PASSWORD@dotdev-club.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

---

## ☁️ Cloudinary Setup (File Storage)

### 1. Create Account
1. Visit: https://cloudinary.com/users/register_free
2. Sign up (25GB free storage)
3. Verify email

### 2. Get Credentials
```
Dashboard → Account Details
- Cloud Name: dxxxxx
- API Key: 123456789012345
- API Secret: xxxxxxxxxxxxxxxxx
```

### 3. Create Upload Preset
```
Settings → Upload → Upload Presets
- Click "Add upload preset"
- Preset name: dotdev_club
- Signing Mode: Unsigned
- Folder: dotdev-club
- Save
```

---

## 📦 Update Flutter Project

### Step 1: Update Dependencies
```bash
cd C:\Users\joelm\.gemini\antigravity\scratch\dotdev_club
flutter pub remove cloud_firestore firebase_storage
flutter pub add mongo_dart cloudinary_public http
```

### Step 2: Update Configuration Files

#### `lib/services/mongodb_service.dart`
```dart
static const String CONNECTION_STRING = 'mongodb+srv://dotdev_admin:YOUR_PASSWORD@dotdev-club.xxxxx.mongodb.net/?retryWrites=true&w=majority';
```

#### `lib/services/storage_service_cloudinary.dart`
```dart
static const String CLOUD_NAME = 'YOUR_CLOUD_NAME';
static const String UPLOAD_PRESET = 'dotdev_club';
```

### Step 3: Update main.dart
```dart
import 'services/mongodb_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Firebase (Auth only)
  await Firebase.initializeApp(...);
  
  // MongoDB
  await MongoDBService.connect();
  
  runApp(const MyApp());
}
```

---

## 🧪 Test Connection

Add this test button anywhere in your app:

```dart
ElevatedButton(
  onPressed: () async {
    try {
      // Test MongoDB
      final users = await MongoDBService.users.find().toList();
      print('✅ MongoDB: ${users.length} users');
      
      // Test Cloudinary
      final storage = StorageService();
      print('✅ Cloudinary configured');
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('✅ All services connected!')),
      );
    } catch (e) {
      print('❌ Error: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('❌ Connection failed: $e')),
      );
    }
  },
  child: Text('Test Connections'),
)
```

---

## 📊 Collections Structure

Your MongoDB database will have these collections:

```
dotdev_club/
├── users
│   ├── _id (ObjectId)
│   ├── email
│   ├── name
│   ├── role
│   └── teamId
├── projects
│   ├── _id (ObjectId)
│   ├── title
│   ├── userId
│   ├── teamId
│   └── fileUrls (Cloudinary URLs)
├── teams
│   ├── _id (ObjectId)
│   ├── name
│   ├── leaderId
│   └── memberIds
├── attendance
│   ├── _id (ObjectId)
│   ├── userId
│   ├── sessionDate
│   └── isPresent
└── joinRequests
    ├── _id (ObjectId)
    ├── userId
    ├── teamId
    └── status
```

---

## 🔄 Migration Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user created
- [ ] Network access configured
- [ ] Connection string obtained
- [ ] Cloudinary account created
- [ ] Upload preset created
- [ ] Dependencies updated in pubspec.yaml
- [ ] mongodb_service.dart configured
- [ ] storage_service_cloudinary.dart configured
- [ ] main.dart updated
- [ ] Tested connections
- [ ] Updated database_service.dart (if needed)
- [ ] Tested file uploads
- [ ] Tested all CRUD operations

---

## 🆘 Common Issues

### "Connection timeout"
```
✓ Check MongoDB IP whitelist (0.0.0.0/0 for development)
✓ Verify connection string is correct
✓ Check internet connection
```

### "Authentication failed"
```
✓ Verify password in connection string
✓ Check database user exists
✓ Ensure user has correct permissions
```

### "Upload failed"
```
✓ Verify Cloudinary cloud name
✓ Check upload preset exists and is unsigned
✓ Verify file size is within limits
```

---

## 💡 Pro Tips

1. **Environment Variables**: Use `flutter_dotenv` to store credentials securely
2. **Offline Support**: Use `hive` or `sqflite` for local caching
3. **Real-time Updates**: Consider WebSockets or polling for live data
4. **Image Optimization**: Use Cloudinary transformations for responsive images
5. **Backup**: Enable MongoDB Atlas automatic backups

---

## 📚 Resources

- [MongoDB Atlas Docs](https://www.mongodb.com/docs/atlas/)
- [Cloudinary Flutter Guide](https://cloudinary.com/documentation/flutter_integration)
- [mongo_dart Package](https://pub.dev/packages/mongo_dart)
- [cloudinary_public Package](https://pub.dev/packages/cloudinary_public)

---

**Ready to migrate? Follow the steps above! 🚀**
