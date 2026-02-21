import 'package:mongo_dart/mongo_dart.dart';
import '../config/app_config.dart';

/// MongoDB Service
/// Handles all database operations using MongoDB Atlas (FREE TIER)
class MongoDBService {
  static MongoDBService? _instance;
  static Db? _db;
  
  MongoDBService._();
  
  static MongoDBService get instance {
    _instance ??= MongoDBService._();
    return _instance!;
  }

  /// Initialize MongoDB connection
  Future<void> connect() async {
    try {
      if (_db != null && _db!.isConnected) {
        print('MongoDB already connected');
        return;
      }

      _db = await Db.create(AppConfig.mongoDbUrl);
      await _db!.open();
      
      print('✅ MongoDB Connected Successfully');
      
      // Create indexes for better performance
      await _createIndexes();
    } catch (e) {
      print('❌ MongoDB Connection Error: $e');
      rethrow;
    }
  }

  /// Create database indexes
  Future<void> _createIndexes() async {
    try {
      // Users collection indexes
      final usersCollection = _db!.collection(AppConfig.usersCollection);
      await usersCollection.createIndex(key: 'uid', unique: true);
      await usersCollection.createIndex(key: 'email', unique: true);
      
      // Attendance collection indexes
      final attendanceCollection = _db!.collection(AppConfig.attendanceCollection);
      await attendanceCollection.createIndex(keys: {'userId': 1, 'date': 1});
      
      // Projects collection indexes
      final projectsCollection = _db!.collection(AppConfig.projectsCollection);
      await projectsCollection.createIndex(key: 'userId');
      await projectsCollection.createIndex(key: 'teamId');
      
      print('✅ Database indexes created');
    } catch (e) {
      print('⚠️ Index creation warning: $e');
    }
  }

  /// Get database instance
  Db get database {
    if (_db == null || !_db!.isConnected) {
      throw Exception('MongoDB not connected. Call connect() first.');
    }
    return _db!;
  }

  /// Get a collection
  DbCollection collection(String collectionName) {
    return database.collection(collectionName);
  }

  /// Close database connection
  Future<void> close() async {
    if (_db != null && _db!.isConnected) {
      await _db!.close();
      print('MongoDB connection closed');
    }
  }

  /// Check if connected
  bool get isConnected => _db != null && _db!.isConnected;
}
