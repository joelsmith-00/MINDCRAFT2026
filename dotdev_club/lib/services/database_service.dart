import 'package:mongo_dart/mongo_dart.dart';
import 'dart:io';
import '../models/project_model.dart';
import '../models/attendance_model.dart';
import '../models/team_model.dart';
import '../models/user_model.dart';
import 'mongodb_service.dart';
import 'storage_service_cloudinary.dart';

class DatabaseService {
  final StorageService _storage = StorageService();

  // ===== PROJECT METHODS =====
  
  Future<String> createProject(ProjectModel project) async {
    final collection = MongoDBService.projects;
    final projectData = project.toMap();
    
    // Insert and get the result
    final result = await collection.insertOne(projectData);
    
    // Return the inserted ID as string
    return result.id.toString();
  }

  Stream<List<ProjectModel>> getProjects({String? userId, String? teamId}) async* {
    final collection = MongoDBService.projects;
    
    // Poll for updates every 2 seconds (simulates real-time)
    while (true) {
      try {
        // Build query selector
        SelectorBuilder selector = where;
        
        if (userId != null) {
          selector = selector.eq('userId', userId);
        }
        if (teamId != null) {
          selector = selector.eq('teamId', teamId);
        }
        
        // Sort by createdAt descending
        selector = selector.sortBy('createdAt', descending: true);
        
        // Fetch documents
        final docs = await collection.find(selector).toList();
        
        // Convert to ProjectModel list
        final projects = docs.map((doc) {
          return ProjectModel.fromMap(doc, doc['_id'].toString());
        }).toList();
        
        yield projects;
        
        // Wait before next poll
        await Future.delayed(Duration(seconds: 2));
      } catch (e) {
        print('Error fetching projects: $e');
        yield [];
        await Future.delayed(Duration(seconds: 2));
      }
    }
  }

  Future<void> updateProject(String projectId, Map<String, dynamic> data) async {
    final collection = MongoDBService.projects;
    
    // Add updatedAt timestamp
    data['updatedAt'] = DateTime.now().toIso8601String();
    
    await collection.updateOne(
      where.id(ObjectId.fromHexString(projectId)),
      ModifierBuilder()
        ..set('updatedAt', data['updatedAt'])
        ..setAll(data),
    );
  }

  Future<void> deleteProject(String projectId) async {
    final collection = MongoDBService.projects;
    
    // Optional: Delete associated files from Cloudinary
    // Get project first to find file URLs
    final project = await collection.findOne(where.id(ObjectId.fromHexString(projectId)));
    
    if (project != null) {
      // Delete files from Cloudinary
      if (project['fileUrls'] != null) {
        for (String url in project['fileUrls']) {
          try {
            String publicId = _storage.getPublicIdFromUrl(url);
            await _storage.deleteFile(publicId);
          } catch (e) {
            print('Error deleting file: $e');
          }
        }
      }
      
      // Delete images from Cloudinary
      if (project['imageUrls'] != null) {
        for (String url in project['imageUrls']) {
          try {
            String publicId = _storage.getPublicIdFromUrl(url);
            await _storage.deleteFile(publicId);
          } catch (e) {
            print('Error deleting image: $e');
          }
        }
      }
    }
    
    // Delete project from MongoDB
    await collection.deleteOne(where.id(ObjectId.fromHexString(projectId)));
  }

  // ===== ATTENDANCE METHODS =====
  
  Future<void> markAttendance(AttendanceModel attendance) async {
    final collection = MongoDBService.attendance;
    await collection.insertOne(attendance.toMap());
  }

  Stream<List<AttendanceModel>> getAttendance({String? userId, String? teamId}) async* {
    final collection = MongoDBService.attendance;
    
    while (true) {
      try {
        SelectorBuilder selector = where;
        
        if (userId != null) {
          selector = selector.eq('userId', userId);
        }
        if (teamId != null) {
          selector = selector.eq('teamId', teamId);
        }
        
        selector = selector.sortBy('sessionDate', descending: true);
        
        final docs = await collection.find(selector).toList();
        final attendance = docs.map((doc) {
          return AttendanceModel.fromMap(doc, doc['_id'].toString());
        }).toList();
        
        yield attendance;
        await Future.delayed(Duration(seconds: 2));
      } catch (e) {
        print('Error fetching attendance: $e');
        yield [];
        await Future.delayed(Duration(seconds: 2));
      }
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
      try {
        final docs = await collection.find().toList();
        final teams = docs.map((doc) {
          return TeamModel.fromMap(doc, doc['_id'].toString());
        }).toList();
        
        yield teams;
        await Future.delayed(Duration(seconds: 2));
      } catch (e) {
        print('Error fetching teams: $e');
        yield [];
        await Future.delayed(Duration(seconds: 2));
      }
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
    
    while (true) {
      try {
        SelectorBuilder selector = where.eq('status', 'pending');
        
        if (teamLeaderId != null) {
          selector = selector.eq('teamLeaderId', teamLeaderId);
        }
        
        final docs = await collection.find(selector).toList();
        final requests = docs.map((doc) {
          return JoinRequest.fromMap(doc, doc['_id'].toString());
        }).toList();
        
        yield requests;
        await Future.delayed(Duration(seconds: 2));
      } catch (e) {
        print('Error fetching join requests: $e');
        yield [];
        await Future.delayed(Duration(seconds: 2));
      }
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
      where.eq('_id', userId),
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
      try {
        final docs = await collection.find().toList();
        final users = docs.map((doc) {
          return UserModel.fromMap(doc, doc['_id'].toString());
        }).toList();
        
        yield users;
        await Future.delayed(Duration(seconds: 2));
      } catch (e) {
        print('Error fetching users: $e');
        yield [];
        await Future.delayed(Duration(seconds: 2));
      }
    }
  }

  Stream<List<UserModel>> getTeamMembers(String teamId) async* {
    final collection = MongoDBService.users;
    
    while (true) {
      try {
        final docs = await collection.find(where.eq('teamId', teamId)).toList();
        final users = docs.map((doc) {
          return UserModel.fromMap(doc, doc['_id'].toString());
        }).toList();
        
        yield users;
        await Future.delayed(Duration(seconds: 2));
      } catch (e) {
        print('Error fetching team members: $e');
        yield [];
        await Future.delayed(Duration(seconds: 2));
      }
    }
  }

  // ===== FILE UPLOAD (Cloudinary) =====
  
  /// Upload file to Cloudinary
  /// Returns the secure URL of the uploaded file
  Future<String> uploadFile(File file, String path) async {
    try {
      // Extract folder from path (e.g., 'projects/user123')
      String folder = path.split('/').take(2).join('/');
      
      // Upload to Cloudinary
      String url = await _storage.uploadFile(file, folder);
      
      return url;
    } catch (e) {
      print('Error uploading file: $e');
      rethrow;
    }
  }
}
