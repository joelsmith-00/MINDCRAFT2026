/// Application Configuration
/// Contains all configuration constants for the Dot Dev Club App
class AppConfig {
  // App Information
  static const String appName = 'Dot Dev Club';
  static const String appVersion = '1.0.0';
  
  // MongoDB Atlas Configuration (FREE TIER)
  // Replace with your MongoDB Atlas connection string
  static const String mongoDbUrl = 'YOUR_MONGODB_ATLAS_CONNECTION_STRING';
  static const String databaseName = 'dotdev_club';
  
  // Collections
  static const String usersCollection = 'users';
  static const String teamsCollection = 'teams';
  static const String projectsCollection = 'projects';
  static const String attendanceCollection = 'attendance';
  static const String teamRequestsCollection = 'team_requests';
  
  // Cloudinary Configuration (FREE TIER)
  // Replace with your Cloudinary credentials
  static const String cloudinaryCloudName = 'YOUR_CLOUD_NAME';
  static const String cloudinaryApiKey = 'YOUR_API_KEY';
  static const String cloudinaryUploadPreset = 'YOUR_UPLOAD_PRESET';
  
  // Firebase Configuration (for Authentication only)
  // Configure via google-services.json and GoogleService-Info.plist
  
  // User Roles
  static const String roleAdmin = 'admin';
  static const String roleTeamLeader = 'team_leader';
  static const String roleMember = 'member';
  
  // Attendance Status
  static const String attendancePresent = 'present';
  static const String attendanceAbsent = 'absent';
  static const String attendanceLate = 'late';
  static const String attendanceLeave = 'leave';
  
  // Project Status
  static const String projectSubmitted = 'submitted';
  static const String projectApproved = 'approved';
  static const String projectNeedsCorrection = 'needs_correction';
  
  // File Upload Limits
  static const int maxFileSize = 10 * 1024 * 1024; // 10 MB
  static const List<String> allowedFileTypes = ['pdf', 'zip', 'jpg', 'png'];
}
