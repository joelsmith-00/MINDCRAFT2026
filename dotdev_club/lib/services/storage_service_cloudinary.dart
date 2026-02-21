import 'dart:io';
import 'package:cloudinary_public/cloudinary_public.dart';

/// Cloudinary file storage service
/// Replaces Firebase Storage for file uploads
class StorageService {
  // TODO: Replace with your Cloudinary credentials
  static const String CLOUD_NAME = 'YOUR_CLOUD_NAME_HERE';
  static const String UPLOAD_PRESET = 'dotdev_club'; // Create this in Cloudinary dashboard
  
  final CloudinaryPublic _cloudinary = CloudinaryPublic(CLOUD_NAME, UPLOAD_PRESET);

  /// Upload a single file to Cloudinary
  /// 
  /// [file] - The file to upload
  /// [folder] - Folder path in Cloudinary (e.g., 'projects/user123')
  /// 
  /// Returns the secure HTTPS URL of the uploaded file
  Future<String> uploadFile(File file, String folder) async {
    try {
      print('📤 Uploading file to Cloudinary...');
      
      CloudinaryResponse response = await _cloudinary.uploadFile(
        CloudinaryFile.fromFile(
          file.path,
          folder: folder,
          resourceType: CloudinaryResourceType.Auto,
        ),
      );
      
      print('✅ Upload successful: ${response.secureUrl}');
      return response.secureUrl;
    } catch (e) {
      print('❌ Upload error: $e');
      rethrow;
    }
  }

  /// Upload multiple files at once
  /// 
  /// [files] - List of files to upload
  /// [folder] - Folder path in Cloudinary
  /// 
  /// Returns list of secure URLs
  Future<List<String>> uploadMultipleFiles(List<File> files, String folder) async {
    List<String> urls = [];
    
    print('📤 Uploading ${files.length} files...');
    
    for (int i = 0; i < files.length; i++) {
      print('Uploading file ${i + 1}/${files.length}...');
      String url = await uploadFile(files[i], folder);
      urls.add(url);
    }
    
    print('✅ All files uploaded successfully');
    return urls;
  }

  /// Upload image with transformation options
  /// 
  /// [file] - Image file to upload
  /// [folder] - Folder path
  /// [width] - Optional max width
  /// [height] - Optional max height
  /// [quality] - Image quality (1-100)
  Future<String> uploadImage(
    File file,
    String folder, {
    int? width,
    int? height,
    int quality = 80,
  }) async {
    try {
      print('📤 Uploading image to Cloudinary...');
      
      CloudinaryResponse response = await _cloudinary.uploadFile(
        CloudinaryFile.fromFile(
          file.path,
          folder: folder,
          resourceType: CloudinaryResourceType.Image,
        ),
      );
      
      // Apply transformations if specified
      String url = response.secureUrl;
      if (width != null || height != null) {
        // Cloudinary URL transformation
        url = url.replaceFirst('/upload/', '/upload/w_${width ?? 'auto'},h_${height ?? 'auto'},q_$quality/');
      }
      
      print('✅ Image uploaded: $url');
      return url;
    } catch (e) {
      print('❌ Image upload error: $e');
      rethrow;
    }
  }

  /// Delete a file from Cloudinary
  /// 
  /// [publicId] - The public ID of the file (from URL)
  /// Example: For URL "https://res.cloudinary.com/demo/image/upload/v1234/sample.jpg"
  /// Public ID is "sample"
  Future<void> deleteFile(String publicId) async {
    try {
      print('🗑️ Deleting file from Cloudinary...');
      await _cloudinary.deleteFile(publicId);
      print('✅ File deleted successfully');
    } catch (e) {
      print('❌ Delete error: $e');
      rethrow;
    }
  }

  /// Extract public ID from Cloudinary URL
  /// 
  /// Example: "https://res.cloudinary.com/demo/image/upload/v1234/folder/sample.jpg"
  /// Returns: "folder/sample"
  String getPublicIdFromUrl(String url) {
    try {
      final uri = Uri.parse(url);
      final pathSegments = uri.pathSegments;
      
      // Find 'upload' segment and get everything after version
      int uploadIndex = pathSegments.indexOf('upload');
      if (uploadIndex != -1 && uploadIndex + 2 < pathSegments.length) {
        // Skip 'upload' and version (v1234567890)
        final publicIdParts = pathSegments.sublist(uploadIndex + 2);
        final publicId = publicIdParts.join('/');
        
        // Remove file extension
        return publicId.replaceAll(RegExp(r'\.[^.]+$'), '');
      }
      
      throw Exception('Invalid Cloudinary URL format');
    } catch (e) {
      print('❌ Error extracting public ID: $e');
      rethrow;
    }
  }

  /// Get optimized image URL with transformations
  /// 
  /// [url] - Original Cloudinary URL
  /// [width] - Target width
  /// [height] - Target height
  /// [quality] - Image quality (1-100)
  String getOptimizedUrl(
    String url, {
    int? width,
    int? height,
    int quality = 80,
  }) {
    if (!url.contains('cloudinary.com')) {
      return url; // Not a Cloudinary URL
    }
    
    String transformation = 'w_${width ?? 'auto'},h_${height ?? 'auto'},q_$quality,f_auto';
    return url.replaceFirst('/upload/', '/upload/$transformation/');
  }
}
