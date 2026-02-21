import 'package:mongo_dart/mongo_dart.dart';

/// Team Model
/// Represents a team in the Dot Dev Club
class TeamModel {
  final ObjectId? id;
  final String name;
  final String description;
  final String leaderId; // User UID
  final List<String> memberIds; // List of User UIDs
  final DateTime createdAt;
  final DateTime updatedAt;

  TeamModel({
    this.id,
    required this.name,
    required this.description,
    required this.leaderId,
    List<String>? memberIds,
    DateTime? createdAt,
    DateTime? updatedAt,
  })  : memberIds = memberIds ?? [],
        createdAt = createdAt ?? DateTime.now(),
        updatedAt = updatedAt ?? DateTime.now();

  // Convert to Map for MongoDB
  Map<String, dynamic> toMap() {
    return {
      if (id != null) '_id': id,
      'name': name,
      'description': description,
      'leaderId': leaderId,
      'memberIds': memberIds,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt.toIso8601String(),
    };
  }

  // Create from Map
  factory TeamModel.fromMap(Map<String, dynamic> map) {
    return TeamModel(
      id: map['_id'] as ObjectId?,
      name: map['name'] as String,
      description: map['description'] as String,
      leaderId: map['leaderId'] as String,
      memberIds: List<String>.from(map['memberIds'] as List? ?? []),
      createdAt: DateTime.parse(map['createdAt'] as String),
      updatedAt: DateTime.parse(map['updatedAt'] as String),
    );
  }

  // Copy with method
  TeamModel copyWith({
    ObjectId? id,
    String? name,
    String? description,
    String? leaderId,
    List<String>? memberIds,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return TeamModel(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      leaderId: leaderId ?? this.leaderId,
      memberIds: memberIds ?? this.memberIds,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? DateTime.now(),
    );
  }

  int get memberCount => memberIds.length;
}
