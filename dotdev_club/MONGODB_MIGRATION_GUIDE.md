# MongoDB Atlas Migration Guide for DOTDEV Club App

## 🎯 Overview

This guide will help you migrate from Firebase (Firestore + Storage) to MongoDB Atlas with a cloud storage solution.

### Architecture Change:
- **Before:** Firebase Auth + Firestore + Firebase Storage
- **After:** Firebase Auth (keep) + MongoDB Atlas + Cloudinary/AWS S3

> **Note:** We'll keep Firebase Auth because it's excellent for authentication. MongoDB Atlas will replace Firestore for data storage, and we'll use Cloudinary (free tier) for file storage.

---

## 📋 Prerequisites

1. MongoDB Atlas account (free tier available)
2. Cloudinary account (free tier: 25GB storage, 25GB bandwidth/month)
3. Flutter app with current Firebase setup

---

## 🚀 Quick Start (30 Minutes)

### Step 1: Create MongoDB Atlas Cluster

1. Go to https://www.mongodb.com/cloud/atlas/register
2. Sign up for free account
3. Create a new cluster:
   - Choose **FREE** tier (M0 Sandbox)
   - Select cloud provider (AWS recommended)
   - Choose region closest to you
   - Cluster name: `dotdev-club`
   - Click **Create Cluster**

### Step 2: Configure Database Access

1. In Atlas dashboard, go to **Database Access** (left sidebar)
2. Click **Add New Database User**
3. Choose **Password** authentication
4. Username: `dotdev_admin`
5. Password: Generate a secure password (save it!)
6. Database User Privileges: **Atlas admin**
7. Click **Add User**

### Step 3: Configure Network Access

1. Go to **Network Access** (left sidebar)
2. Click **Add IP Address**
3. Click **Allow Access from Anywhere** (for development)
   - For production, restrict to specific IPs
4. Click **Confirm**

### Step 4: Get Connection String

1. Go to **Database** (left sidebar)
2. Click **Connect** on your cluster
3. Choose **Connect your application**
4. Driver: **Dart** (or use Node.js driver format)
5. Copy the connection string:
   ```
   mongodb+srv://dotdev_admin:<password>@dotdev-club.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<password>` with your actual password
7. Save this connection string securely

### Step 5: Create Cloudinary Account

1. Go to https://cloudinary.com/users/register_free
2. Sign up for free account
3. After login, go to **Dashboard**
4. Note these credentials:
   - **Cloud Name**: `dxxxxxx`
   - **API Key**: `123456789012345`
   - **API Secret**: `xxxxxxxxxxxxxxxxxxxx`

---

## 📦 Update Flutter Dependencies

### 1. Update `pubspec.yaml`

Replace Firebase dependencies with MongoDB and Cloudinary:

```yaml
dependencies:
  flutter:
    sdk: flutter

  # UI & Icons
  cupertino_icons: ^1.0.8
  google_fonts: ^6.1.0
  
  # State Management
  provider: ^6.1.1
  
  # Authentication (Keep Firebase Auth)
  firebase_core: ^2.24.2
  firebase_auth: ^4.16.0
  
  # MongoDB (NEW - replaces Firestore)
  mongo_dart: ^0.9.3
  
  # File Storage (NEW - replaces Firebase Storage)
  cloudinary_public: ^0.21.0
  
  # HTTP for API calls
  http: ^1.2.0
  
  # File & Image Handling
  image_picker: ^1.0.7
  file_picker: ^6.1.1
  
  # Utilities
  intl: ^0.19.0
  uuid: ^4.3.3
  
  # Animations
  animated_text_kit: ^4.2.2
  lottie: ^3.0.0
```

### 2. Remove Firebase dependencies

```bash
flutter pub remove cloud_firestore firebase_storage
```

### 3. Add new dependencies

```bash
flutter pub add mongo_dart cloudinary_public http
```

---

## 🔧 Create MongoDB Service

Create a new file: `lib/services/mongodb_service.dart`

```dart
import 'package:mongo_dart/mongo_dart.dart';

class MongoDBService {
  static Db? _db;
  static const String CONNECTION_STRING = 'YOUR_MONGODB_CONNECTION_STRING_HERE';
  static const String DATABASE_NAME = 'dotdev_club';

  // Initialize connection
  static Future<void> connect() async {
    try {
      _db = await Db.create(CONNECTION_STRING);
      await _db!.open();
      print('✅ Connected to MongoDB Atlas');
    } catch (e) {
      print('❌ MongoDB connection error: $e');
      rethrow;
    }
  }

  // Get database instance
  static Db get db {
    if (_db == null) {
      throw Exception('Database not initialized. Call connect() first.');
    }
    return _db!;
  }

  // Get collection
  static DbCollection collection(String collectionName) {
    return db.collection(collectionName);
  }

  // Close connection
  static Future<void> close() async {
    await _db?.close();
  }

  // Collections
  static DbCollection get users => collection('users');
  static DbCollection get projects => collection('projects');
  static DbCollection get teams => collection('teams');
  static DbCollection get attendance => collection('attendance');
  static DbCollection get joinRequests => collection('joinRequests');
}
```

---

## 🗄️ Create New Database Service

Create: `lib/services/database_service_mongodb.dart`

```dart
import 'package:mongo_dart/mongo_dart.dart';
import 'mongodb_service.dart';
import '../models/project_model.dart';
import '../models/attendance_model.dart';
import '../models/team_model.dart';
import '../models/user_model.dart';

class DatabaseService {
  // ===== PROJECT METHODS =====
  
  Future<String> createProject(ProjectModel project) async {
    final collection = MongoDBService.projects;
    final result = await collection.insertOne(project.toMap());
    return result.id.toString();
  }

  Stream<List<ProjectModel>> getProjects({String? userId, String? teamId}) async* {
    final collection = MongoDBService.projects;
    
    // Build query
    final selector = where;
    if (userId != null) {
      selector.eq('userId', userId);
    }
    if (teamId != null) {
      selector.eq('teamId', teamId);
    }
    
    // Sort by createdAt descending
    selector.sortBy('createdAt', descending: true);
    
    while (true) {
      final docs = await collection.find(selector).toList();
      yield docs.map((doc) => ProjectModel.fromMap(doc, doc['_id'].toString())).toList();
      await Future.delayed(Duration(seconds: 2)); // Poll every 2 seconds
    }
  }

  Future<void> updateProject(String projectId, Map<String, dynamic> data) async {
    final collection = MongoDBService.projects;
    await collection.updateOne(
      where.id(ObjectId.fromHexString(projectId)),
      modify.set('updatedAt', DateTime.now().toIso8601String())
        ..setAll(data),
    );
  }

  Future<void> deleteProject(String projectId) async {
    final collection = MongoDBService.projects;
    await collection.deleteOne(where.id(ObjectId.fromHexString(projectId)));
  }

  // ===== ATTENDANCE METHODS =====
  
  Future<void> markAttendance(AttendanceModel attendance) async {
    final collection = MongoDBService.attendance;
    await collection.insertOne(attendance.toMap());
  }

  Stream<List<AttendanceModel>> getAttendance({String? userId, String? teamId}) async* {
    final collection = MongoDBService.attendance;
    
    final selector = where;
    if (userId != null) {
      selector.eq('userId', userId);
    }
    if (teamId != null) {
      selector.eq('teamId', teamId);
    }
    
    selector.sortBy('sessionDate', descending: true);
    
    while (true) {
      final docs = await collection.find(selector).toList();
      yield docs.map((doc) => AttendanceModel.fromMap(doc, doc['_id'].toString())).toList();
      await Future.delayed(Duration(seconds: 2));
    }
  }

  Future<AttendanceStats> getAttendanceStats(String userId) async {
    final collection = MongoDBService.attendance;
    final docs = await collection.find(where.eq('userId', userId)).toList();
    
    int total = docs.length;
    int attended = docs.where((doc) => doc['isPresent'] == true).length;
    
    return AttendanceStats(totalSessions: total, attendedSessions: attended);
  }

  // ===== TEAM METHODS =====
  
  Future<String> createTeam(TeamModel team) async {
    final collection = MongoDBService.teams;
    final result = await collection.insertOne(team.toMap());
    return result.id.toString();
  }

  Stream<List<TeamModel>> getTeams() async* {
    final collection = MongoDBService.teams;
    
    while (true) {
      final docs = await collection.find().toList();
      yield docs.map((doc) => TeamModel.fromMap(doc, doc['_id'].toString())).toList();
      await Future.delayed(Duration(seconds: 2));
    }
  }

  Future<TeamModel?> getTeam(String teamId) async {
    final collection = MongoDBService.teams;
    final doc = await collection.findOne(where.id(ObjectId.fromHexString(teamId)));
    if (doc != null) {
      return TeamModel.fromMap(doc, doc['_id'].toString());
    }
    return null;
  }

  // ===== JOIN REQUEST METHODS =====
  
  Future<void> createJoinRequest(JoinRequest request) async {
    final collection = MongoDBService.joinRequests;
    await collection.insertOne(request.toMap());
  }

  Stream<List<JoinRequest>> getJoinRequests({String? teamLeaderId}) async* {
    final collection = MongoDBService.joinRequests;
    
    final selector = where.eq('status', 'pending');
    if (teamLeaderId != null) {
      selector.eq('teamLeaderId', teamLeaderId);
    }
    
    while (true) {
      final docs = await collection.find(selector).toList();
      yield docs.map((doc) => JoinRequest.fromMap(doc, doc['_id'].toString())).toList();
      await Future.delayed(Duration(seconds: 2));
    }
  }

  Future<void> approveJoinRequest(String requestId, String userId, String teamId) async {
    // Update request status
    await MongoDBService.joinRequests.updateOne(
      where.id(ObjectId.fromHexString(requestId)),
      modify.set('status', 'approved'),
    );

    // Update user
    await MongoDBService.users.updateOne(
      where.id(ObjectId.fromHexString(userId)),
      modify.set('teamId', teamId).set('isApproved', true),
    );

    // Add to team members
    TeamModel? team = await getTeam(teamId);
    if (team != null) {
      List<String> members = List.from(team.memberIds);
      members.add(userId);
      await MongoDBService.teams.updateOne(
        where.id(ObjectId.fromHexString(teamId)),
        modify.set('memberIds', members),
      );
    }
  }

  Future<void> rejectJoinRequest(String requestId) async {
    await MongoDBService.joinRequests.updateOne(
      where.id(ObjectId.fromHexString(requestId)),
      modify.set('status', 'rejected'),
    );
  }

  // ===== USER METHODS =====
  
  Stream<List<UserModel>> getAllUsers() async* {
    final collection = MongoDBService.users;
    
    while (true) {
      final docs = await collection.find().toList();
      yield docs.map((doc) => UserModel.fromMap(doc, doc['_id'].toString())).toList();
      await Future.delayed(Duration(seconds: 2));
    }
  }

  Stream<List<UserModel>> getTeamMembers(String teamId) async* {
    final collection = MongoDBService.users;
    
    while (true) {
      final docs = await collection.find(where.eq('teamId', teamId)).toList();
      yield docs.map((doc) => UserModel.fromMap(doc, doc['_id'].toString())).toList();
      await Future.delayed(Duration(seconds: 2));
    }
  }
}
```

---

## ☁️ Create Cloudinary Storage Service

Create: `lib/services/storage_service.dart`

```dart
import 'dart:io';
import 'package:cloudinary_public/cloudinary_public.dart';

class StorageService {
  static const String CLOUD_NAME = 'YOUR_CLOUD_NAME';
  static const String UPLOAD_PRESET = 'dotdev_club'; // Create this in Cloudinary
  
  final CloudinaryPublic _cloudinary = CloudinaryPublic(CLOUD_NAME, UPLOAD_PRESET);

  /// Upload file to Cloudinary
  /// Returns the secure URL of uploaded file
  Future<String> uploadFile(File file, String folder) async {
    try {
      CloudinaryResponse response = await _cloudinary.uploadFile(
        CloudinaryFile.fromFile(
          file.path,
          folder: folder,
          resourceType: CloudinaryResourceType.Auto,
        ),
      );
      
      return response.secureUrl;
    } catch (e) {
      print('❌ Upload error: $e');
      rethrow;
    }
  }

  /// Upload multiple files
  Future<List<String>> uploadMultipleFiles(List<File> files, String folder) async {
    List<String> urls = [];
    
    for (File file in files) {
      String url = await uploadFile(file, folder);
      urls.add(url);
    }
    
    return urls;
  }

  /// Delete file from Cloudinary
  Future<void> deleteFile(String publicId) async {
    try {
      await _cloudinary.deleteFile(publicId);
    } catch (e) {
      print('❌ Delete error: $e');
      rethrow;
    }
  }
}
```

---

## 🔄 Update main.dart

Replace Firebase initialization:

```dart
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:provider/provider.dart';
import 'services/mongodb_service.dart';
import 'providers/user_provider.dart';
import 'screens/auth_screen.dart';
import 'screens/home_screen.dart';
import 'utils/theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase (for Auth only)
  await Firebase.initializeApp(
    options: const FirebaseOptions(
      apiKey: 'YOUR_API_KEY',
      appId: 'YOUR_APP_ID',
      messagingSenderId: 'YOUR_SENDER_ID',
      projectId: 'dotdev-club',
    ),
  );
  
  // Initialize MongoDB
  await MongoDBService.connect();
  
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => UserProvider()),
      ],
      child: MaterialApp(
        title: 'DOTDEV Club',
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        home: StreamBuilder<User?>(
          stream: FirebaseAuth.instance.authStateChanges(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Scaffold(
                body: Center(child: CircularProgressIndicator()),
              );
            }
            
            if (snapshot.hasData) {
              return const HomeScreen();
            }
            
            return const AuthScreen();
          },
        ),
      ),
    );
  }
}
```

---

## 🎨 Setup Cloudinary Upload Preset

1. Login to Cloudinary Dashboard
2. Go to **Settings** → **Upload**
3. Scroll to **Upload presets**
4. Click **Add upload preset**
5. Preset name: `dotdev_club`
6. Signing Mode: **Unsigned**
7. Folder: `dotdev-club`
8. Click **Save**

---

## 🧪 Testing Your Setup

### Test 1: MongoDB Connection
```dart
// In your app, add a test button
ElevatedButton(
  onPressed: () async {
    try {
      final users = await MongoDBService.users.find().toList();
      print('✅ MongoDB connected! Users: ${users.length}');
    } catch (e) {
      print('❌ MongoDB error: $e');
    }
  },
  child: Text('Test MongoDB'),
)
```

### Test 2: File Upload
```dart
// Test Cloudinary upload
ElevatedButton(
  onPressed: () async {
    final picker = ImagePicker();
    final image = await picker.pickImage(source: ImageSource.gallery);
    
    if (image != null) {
      final storage = StorageService();
      final url = await storage.uploadFile(File(image.path), 'test');
      print('✅ Uploaded: $url');
    }
  },
  child: Text('Test Upload'),
)
```

---

## 📊 Data Migration (Optional)

If you have existing Firebase data to migrate:

### Option 1: Manual Export/Import
1. Export Firestore data: Firebase Console → Firestore → Export
2. Convert JSON to MongoDB format
3. Import to MongoDB Atlas using MongoDB Compass

### Option 2: Use Migration Script
Create a Node.js script to migrate data programmatically.

---

## 🔒 Security Best Practices

### MongoDB Atlas:
1. **Never expose connection string in code**
   - Use environment variables
   - For Flutter: Use `flutter_dotenv` package

2. **Enable IP Whitelist** in production
3. **Use Database Rules** to restrict access
4. **Enable Encryption** for sensitive data

### Cloudinary:
1. **Use signed uploads** for production
2. **Set upload restrictions** (file size, types)
3. **Enable moderation** for user uploads

---

## 💰 Cost Comparison

### Free Tier Limits:

**MongoDB Atlas (M0):**
- ✅ 512 MB storage
- ✅ Shared RAM
- ✅ Unlimited connections
- ✅ Perfect for development

**Cloudinary Free:**
- ✅ 25 GB storage
- ✅ 25 GB bandwidth/month
- ✅ 25 credits/month
- ✅ Good for small apps

**Firebase (Spark Plan):**
- ✅ 1 GB storage
- ✅ 10 GB bandwidth/month
- ✅ 50K reads/day
- ✅ 20K writes/day

---

## 🚨 Important Notes

1. **Real-time Updates:** MongoDB doesn't have native real-time listeners like Firestore. The code above uses polling (checking every 2 seconds). For true real-time, consider:
   - MongoDB Change Streams (requires replica set - not available in free tier)
   - WebSocket server
   - Firebase Realtime Database (keep for real-time only)

2. **Offline Support:** Firestore has built-in offline support. With MongoDB, you'll need to implement caching yourself using packages like `hive` or `sqflite`.

3. **Authentication:** We're keeping Firebase Auth because it's excellent and free. You could switch to MongoDB Realm or custom JWT auth if needed.

---

## 📚 Next Steps

1. ✅ Set up MongoDB Atlas cluster
2. ✅ Set up Cloudinary account
3. ✅ Update dependencies
4. ✅ Create MongoDB and Storage services
5. ✅ Update main.dart
6. ✅ Test connections
7. 🎨 Migrate existing code
8. 🧪 Test all features
9. 🚀 Deploy

---

## 🆘 Troubleshooting

### "Connection timeout"
- Check MongoDB IP whitelist
- Verify connection string
- Check internet connection

### "Upload failed"
- Verify Cloudinary credentials
- Check upload preset exists
- Verify file size limits

### "Authentication error"
- Firebase Auth still works the same
- Check Firebase configuration

---

## 📖 Resources

- [MongoDB Atlas Docs](https://www.mongodb.com/docs/atlas/)
- [mongo_dart Package](https://pub.dev/packages/mongo_dart)
- [Cloudinary Docs](https://cloudinary.com/documentation)
- [cloudinary_public Package](https://pub.dev/packages/cloudinary_public)

---

**Happy Coding! 🚀**
**DOTDEV Club - Now with MongoDB Atlas!**
