import 'package:mongo_dart/mongo_dart.dart';

/// Attendance Model
/// Represents daily attendance record for a user
class AttendanceModel {
  final ObjectId? id;
  final String userId;
  final String teamId;
  final DateTime date;
  final String status; // present, absent, late, leave
  final String? remarks;
  final String markedBy; // UID of person who marked attendance
  final DateTime createdAt;

  AttendanceModel({
    this.id,
    required this.userId,
    required this.teamId,
    required this.date,
    required this.status,
    this.remarks,
    required this.markedBy,
    DateTime? createdAt,
  }) : createdAt = createdAt ?? DateTime.now();

  // Convert to Map for MongoDB
  Map<String, dynamic> toMap() {
    return {
      if (id != null) '_id': id,
      'userId': userId,
      'teamId': teamId,
      'date': date.toIso8601String(),
      'status': status,
      'remarks': remarks,
      'markedBy': markedBy,
      'createdAt': createdAt.toIso8601String(),
    };
  }

  // Create from Map
  factory AttendanceModel.fromMap(Map<String, dynamic> map) {
    return AttendanceModel(
      id: map['_id'] as ObjectId?,
      userId: map['userId'] as String,
      teamId: map['teamId'] as String,
      date: DateTime.parse(map['date'] as String),
      status: map['status'] as String,
      remarks: map['remarks'] as String?,
      markedBy: map['markedBy'] as String,
      createdAt: DateTime.parse(map['createdAt'] as String),
    );
  }

  // Copy with method
  AttendanceModel copyWith({
    ObjectId? id,
    String? userId,
    String? teamId,
    DateTime? date,
    String? status,
    String? remarks,
    String? markedBy,
    DateTime? createdAt,
  }) {
    return AttendanceModel(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      teamId: teamId ?? this.teamId,
      date: date ?? this.date,
      status: status ?? this.status,
      remarks: remarks ?? this.remarks,
      markedBy: markedBy ?? this.markedBy,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  bool get isPresent => status == 'present';
  bool get isAbsent => status == 'absent';
  bool get isLate => status == 'late';
  bool get isOnLeave => status == 'leave';
}
