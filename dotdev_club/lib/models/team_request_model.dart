import 'package:mongo_dart/mongo_dart.dart';

/// Team Request Model
/// Represents a request from a member to join a team
class TeamRequestModel {
  final ObjectId? id;
  final String userId;
  final String teamId;
  final String status; // pending, approved, rejected
  final String? message;
  final DateTime requestedAt;
  final DateTime? respondedAt;
  final String? respondedBy; // UID of admin/leader who responded

  TeamRequestModel({
    this.id,
    required this.userId,
    required this.teamId,
    this.status = 'pending',
    this.message,
    DateTime? requestedAt,
    this.respondedAt,
    this.respondedBy,
  }) : requestedAt = requestedAt ?? DateTime.now();

  // Convert to Map for MongoDB
  Map<String, dynamic> toMap() {
    return {
      if (id != null) '_id': id,
      'userId': userId,
      'teamId': teamId,
      'status': status,
      'message': message,
      'requestedAt': requestedAt.toIso8601String(),
      'respondedAt': respondedAt?.toIso8601String(),
      'respondedBy': respondedBy,
    };
  }

  // Create from Map
  factory TeamRequestModel.fromMap(Map<String, dynamic> map) {
    return TeamRequestModel(
      id: map['_id'] as ObjectId?,
      userId: map['userId'] as String,
      teamId: map['teamId'] as String,
      status: map['status'] as String? ?? 'pending',
      message: map['message'] as String?,
      requestedAt: DateTime.parse(map['requestedAt'] as String),
      respondedAt: map['respondedAt'] != null
          ? DateTime.parse(map['respondedAt'] as String)
          : null,
      respondedBy: map['respondedBy'] as String?,
    );
  }

  // Copy with method
  TeamRequestModel copyWith({
    ObjectId? id,
    String? userId,
    String? teamId,
    String? status,
    String? message,
    DateTime? requestedAt,
    DateTime? respondedAt,
    String? respondedBy,
  }) {
    return TeamRequestModel(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      teamId: teamId ?? this.teamId,
      status: status ?? this.status,
      message: message ?? this.message,
      requestedAt: requestedAt ?? this.requestedAt,
      respondedAt: respondedAt ?? this.respondedAt,
      respondedBy: respondedBy ?? this.respondedBy,
    );
  }

  bool get isPending => status == 'pending';
  bool get isApproved => status == 'approved';
  bool get isRejected => status == 'rejected';
}
