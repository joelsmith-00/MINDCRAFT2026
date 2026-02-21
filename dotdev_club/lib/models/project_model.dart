import 'package:mongo_dart/mongo_dart.dart';

/// Project Model
/// Represents a project submission by a team member
class ProjectModel {
  final ObjectId? id;
  final String title;
  final String description;
  final String userId; // Submitter's UID
  final String teamId;
  final List<String> technologies;
  final String? fileUrl; // Cloudinary URL for project file
  final String? githubUrl;
  final String status; // submitted, approved, needs_correction
  final String? feedback;
  final DateTime submittedAt;
  final DateTime? reviewedAt;
  final DateTime updatedAt;

  ProjectModel({
    this.id,
    required this.title,
    required this.description,
    required this.userId,
    required this.teamId,
    List<String>? technologies,
    this.fileUrl,
    this.githubUrl,
    this.status = 'submitted',
    this.feedback,
    DateTime? submittedAt,
    this.reviewedAt,
    DateTime? updatedAt,
  })  : technologies = technologies ?? [],
        submittedAt = submittedAt ?? DateTime.now(),
        updatedAt = updatedAt ?? DateTime.now();

  // Convert to Map for MongoDB
  Map<String, dynamic> toMap() {
    return {
      if (id != null) '_id': id,
      'title': title,
      'description': description,
      'userId': userId,
      'teamId': teamId,
      'technologies': technologies,
      'fileUrl': fileUrl,
      'githubUrl': githubUrl,
      'status': status,
      'feedback': feedback,
      'submittedAt': submittedAt.toIso8601String(),
      'reviewedAt': reviewedAt?.toIso8601String(),
      'updatedAt': updatedAt.toIso8601String(),
    };
  }

  // Create from Map
  factory ProjectModel.fromMap(Map<String, dynamic> map) {
    return ProjectModel(
      id: map['_id'] as ObjectId?,
      title: map['title'] as String,
      description: map['description'] as String,
      userId: map['userId'] as String,
      teamId: map['teamId'] as String,
      technologies: List<String>.from(map['technologies'] as List? ?? []),
      fileUrl: map['fileUrl'] as String?,
      githubUrl: map['githubUrl'] as String?,
      status: map['status'] as String? ?? 'submitted',
      feedback: map['feedback'] as String?,
      submittedAt: DateTime.parse(map['submittedAt'] as String),
      reviewedAt: map['reviewedAt'] != null 
          ? DateTime.parse(map['reviewedAt'] as String) 
          : null,
      updatedAt: DateTime.parse(map['updatedAt'] as String),
    );
  }

  // Copy with method
  ProjectModel copyWith({
    ObjectId? id,
    String? title,
    String? description,
    String? userId,
    String? teamId,
    List<String>? technologies,
    String? fileUrl,
    String? githubUrl,
    String? status,
    String? feedback,
    DateTime? submittedAt,
    DateTime? reviewedAt,
    DateTime? updatedAt,
  }) {
    return ProjectModel(
      id: id ?? this.id,
      title: title ?? this.title,
      description: description ?? this.description,
      userId: userId ?? this.userId,
      teamId: teamId ?? this.teamId,
      technologies: technologies ?? this.technologies,
      fileUrl: fileUrl ?? this.fileUrl,
      githubUrl: githubUrl ?? this.githubUrl,
      status: status ?? this.status,
      feedback: feedback ?? this.feedback,
      submittedAt: submittedAt ?? this.submittedAt,
      reviewedAt: reviewedAt ?? this.reviewedAt,
      updatedAt: updatedAt ?? DateTime.now(),
    );
  }

  bool get isApproved => status == 'approved';
  bool get needsCorrection => status == 'needs_correction';
  bool get isSubmitted => status == 'submitted';
}
