import 'dart:io';
import 'package:cloudinary_public/cloudinary_public.dart';
import '../config/app_config.dart';

/// Cloudinary Service
/// Handles file uploads to Cloudinary (FREE TIER)
class CloudinaryService {
  static CloudinaryService? _instance;
  late CloudinaryPublic _cloudinary;

  CloudinaryService._() {
    _cloudinary = CloudinaryPublic(
      AppConfig.cloudinaryCloudName,
      AppConfig.cloudinaryUploadPreset,
      cache: false,
    );
  }

  static CloudinaryService get instance {
    _instance ??= CloudinaryService._();
    return _instance!;
  }

  /// Upload a file to Cloudinary
  /// Returns the secure URL of the uploaded file
  Future<String> uploadFile({
    required File file,
    required String folder,
    String? publicId,
  }) async {
    try {
      print('📤 Uploading file to Cloudinary...');
      
      final response = await _cloudinary.uploadFile(
        CloudinaryFile.fromFile(
          file.path,
          folder: folder,
          publicId: publicId,
          resourceType: CloudinaryResourceType.Auto,
        ),
      );

      print('✅ File uploaded successfully: ${response.secureUrl}');
      return response.secureUrl;
    } catch (e) {
      print('❌ Cloudinary upload error: $e');
      throw Exception('Failed to upload file: $e');
    }
  }

  /// Upload profile photo
  Future<String> uploadProfilePhoto(File file, String userId) async {
    return await uploadFile(
      file: file,
      folder: 'dotdev_club/profiles',
      publicId: 'profile_$userId',
    );
  }

  /// Upload project file
  Future<String> uploadProjectFile(File file, String projectId) async {
    return await uploadFile(
      file: file,
      folder: 'dotdev_club/projects',
      publicId: 'project_$projectId',
    );
  }

  /// Delete a file from Cloudinary
  Future<void> deleteFile(String publicId) async {
    try {
      // Note: Deletion requires authenticated API calls
      // For free tier, you can manually delete from Cloudinary dashboard
      // or implement server-side deletion
      print('⚠️ File deletion should be done via Cloudinary dashboard or server');
    } catch (e) {
      print('❌ Cloudinary delete error: $e');
    }
  }

  /// Validate file before upload
  bool validateFile(File file) {
    // Check file size
    final fileSize = file.lengthSync();
    if (fileSize > AppConfig.maxFileSize) {
      throw Exception('File size exceeds ${AppConfig.maxFileSize / (1024 * 1024)} MB');
    }

    // Check file extension
    final extension = file.path.split('.').last.toLowerCase();
    if (!AppConfig.allowedFileTypes.contains(extension)) {
      throw Exception('File type .$extension is not allowed');
    }

    return true;
  }
}
