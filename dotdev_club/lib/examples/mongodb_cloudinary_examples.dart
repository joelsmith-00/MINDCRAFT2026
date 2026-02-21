import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'services/mongodb_service.dart';
import 'services/storage_service_cloudinary.dart';

/// Example usage of MongoDB and Cloudinary services
/// This file demonstrates how to use the new services in your app

// ===== EXAMPLE 1: Creating a Project =====

Future<void> createProjectExample() async {
  try {
    // 1. Pick files to upload
    final picker = ImagePicker();
    final images = await picker.pickMultiImage();
    
    if (images.isEmpty) return;
    
    // 2. Upload files to Cloudinary
    final storage = StorageService();
    List<String> fileUrls = [];
    
    for (var image in images) {
      String url = await storage.uploadFile(
        File(image.path),
        'projects/user123', // Folder path
      );
      fileUrls.add(url);
    }
    
    // 3. Create project data
    final projectData = {
      'title': 'My Awesome Project',
      'description': 'This is a test project',
      'userId': 'user123',
      'teamId': 'team456',
      'fileUrls': fileUrls, // Cloudinary URLs
      'createdAt': DateTime.now().toIso8601String(),
      'status': 'active',
    };
    
    // 4. Save to MongoDB
    final result = await MongoDBService.projects.insertOne(projectData);
    
    print('✅ Project created with ID: ${result.id}');
  } catch (e) {
    print('❌ Error creating project: $e');
  }
}

// ===== EXAMPLE 2: Getting All Projects =====

Future<List<Map<String, dynamic>>> getProjectsExample() async {
  try {
    // Get all projects from MongoDB
    final projects = await MongoDBService.projects
        .find()
        .toList();
    
    print('✅ Found ${projects.length} projects');
    return projects;
  } catch (e) {
    print('❌ Error getting projects: $e');
    return [];
  }
}

// ===== EXAMPLE 3: Getting Projects by User =====

Future<List<Map<String, dynamic>>> getUserProjectsExample(String userId) async {
  try {
    // Query projects by userId
    final projects = await MongoDBService.projects
        .find(where.eq('userId', userId))
        .toList();
    
    print('✅ Found ${projects.length} projects for user $userId');
    return projects;
  } catch (e) {
    print('❌ Error getting user projects: $e');
    return [];
  }
}

// ===== EXAMPLE 4: Real-time Stream of Projects =====

Stream<List<Map<String, dynamic>>> getProjectsStreamExample() async* {
  while (true) {
    try {
      // Fetch projects from MongoDB
      final projects = await MongoDBService.projects
          .find()
          .toList();
      
      yield projects;
      
      // Poll every 2 seconds for updates
      await Future.delayed(Duration(seconds: 2));
    } catch (e) {
      print('❌ Error in stream: $e');
      yield [];
    }
  }
}

// ===== EXAMPLE 5: Updating a Project =====

Future<void> updateProjectExample(String projectId) async {
  try {
    await MongoDBService.projects.updateOne(
      where.id(ObjectId.fromHexString(projectId)),
      modify
          .set('title', 'Updated Project Title')
          .set('status', 'completed')
          .set('updatedAt', DateTime.now().toIso8601String()),
    );
    
    print('✅ Project updated successfully');
  } catch (e) {
    print('❌ Error updating project: $e');
  }
}

// ===== EXAMPLE 6: Deleting a Project =====

Future<void> deleteProjectExample(String projectId) async {
  try {
    // 1. Get project to find file URLs
    final project = await MongoDBService.projects
        .findOne(where.id(ObjectId.fromHexString(projectId)));
    
    if (project != null && project['fileUrls'] != null) {
      // 2. Delete files from Cloudinary
      final storage = StorageService();
      for (String url in project['fileUrls']) {
        try {
          String publicId = storage.getPublicIdFromUrl(url);
          await storage.deleteFile(publicId);
        } catch (e) {
          print('⚠️ Error deleting file: $e');
        }
      }
    }
    
    // 3. Delete project from MongoDB
    await MongoDBService.projects.deleteOne(
      where.id(ObjectId.fromHexString(projectId)),
    );
    
    print('✅ Project deleted successfully');
  } catch (e) {
    print('❌ Error deleting project: $e');
  }
}

// ===== EXAMPLE 7: Creating a User =====

Future<void> createUserExample(String uid, String email, String name) async {
  try {
    final userData = {
      '_id': uid, // Use Firebase Auth UID as MongoDB _id
      'email': email,
      'name': name,
      'role': 'member',
      'teamId': null,
      'isApproved': false,
      'createdAt': DateTime.now().toIso8601String(),
    };
    
    await MongoDBService.users.insertOne(userData);
    
    print('✅ User created successfully');
  } catch (e) {
    print('❌ Error creating user: $e');
  }
}

// ===== EXAMPLE 8: Getting User by ID =====

Future<Map<String, dynamic>?> getUserExample(String userId) async {
  try {
    final user = await MongoDBService.users.findOne(
      where.eq('_id', userId),
    );
    
    if (user != null) {
      print('✅ User found: ${user['name']}');
    } else {
      print('⚠️ User not found');
    }
    
    return user;
  } catch (e) {
    print('❌ Error getting user: $e');
    return null;
  }
}

// ===== EXAMPLE 9: Complex Query =====

Future<List<Map<String, dynamic>>> getActiveTeamProjectsExample(String teamId) async {
  try {
    // Get all active projects for a specific team, sorted by date
    final projects = await MongoDBService.projects
        .find(
          where
              .eq('teamId', teamId)
              .eq('status', 'active')
              .sortBy('createdAt', descending: true),
        )
        .toList();
    
    print('✅ Found ${projects.length} active projects for team $teamId');
    return projects;
  } catch (e) {
    print('❌ Error getting team projects: $e');
    return [];
  }
}

// ===== EXAMPLE 10: Upload Image with Optimization =====

Future<String?> uploadOptimizedImageExample(File imageFile) async {
  try {
    final storage = StorageService();
    
    // Upload image with automatic optimization
    String url = await storage.uploadImage(
      imageFile,
      'profile-pictures',
      width: 500,
      height: 500,
      quality: 80,
    );
    
    print('✅ Image uploaded: $url');
    return url;
  } catch (e) {
    print('❌ Error uploading image: $e');
    return null;
  }
}

// ===== EXAMPLE 11: Flutter Widget Using Stream =====

class ProjectsListWidget extends StatelessWidget {
  const ProjectsListWidget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<List<Map<String, dynamic>>>(
      stream: getProjectsStreamExample(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator());
        }
        
        if (snapshot.hasError) {
          return Center(child: Text('Error: ${snapshot.error}'));
        }
        
        if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Center(child: Text('No projects found'));
        }
        
        final projects = snapshot.data!;
        
        return ListView.builder(
          itemCount: projects.length,
          itemBuilder: (context, index) {
            final project = projects[index];
            return ListTile(
              title: Text(project['title'] ?? 'Untitled'),
              subtitle: Text(project['description'] ?? ''),
              trailing: IconButton(
                icon: Icon(Icons.delete),
                onPressed: () {
                  deleteProjectExample(project['_id'].toString());
                },
              ),
            );
          },
        );
      },
    );
  }
}

// ===== EXAMPLE 12: Test Connection Widget =====

class TestConnectionButton extends StatelessWidget {
  const TestConnectionButton({Key? key}) : super(key: key);

  Future<void> _testConnection(BuildContext context) async {
    try {
      // Test MongoDB
      final users = await MongoDBService.users.find().toList();
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('✅ MongoDB connected! Found ${users.length} users'),
          backgroundColor: Colors.green,
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('❌ Connection failed: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () => _testConnection(context),
      child: Text('Test MongoDB Connection'),
    );
  }
}

// ===== EXAMPLE 13: Upload Button Widget =====

class UploadFileButton extends StatelessWidget {
  const UploadFileButton({Key? key}) : super(key: key);

  Future<void> _uploadFile(BuildContext context) async {
    try {
      final picker = ImagePicker();
      final image = await picker.pickImage(source: ImageSource.gallery);
      
      if (image == null) return;
      
      // Show loading
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Uploading...')),
      );
      
      final storage = StorageService();
      String url = await storage.uploadFile(
        File(image.path),
        'test-uploads',
      );
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('✅ Uploaded successfully!\n$url'),
          backgroundColor: Colors.green,
          duration: Duration(seconds: 5),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('❌ Upload failed: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      onPressed: () => _uploadFile(context),
      icon: Icon(Icons.upload),
      label: Text('Upload to Cloudinary'),
    );
  }
}

// ===== USAGE IN YOUR APP =====

/*
// In your main.dart:
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase
  await Firebase.initializeApp(...);
  
  // Initialize MongoDB
  await MongoDBService.connect();
  
  runApp(MyApp());
}

// In your screens:
class MyScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('DOTDEV Club')),
      body: Column(
        children: [
          TestConnectionButton(),
          UploadFileButton(),
          Expanded(child: ProjectsListWidget()),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: createProjectExample,
        child: Icon(Icons.add),
      ),
    );
  }
}
*/
