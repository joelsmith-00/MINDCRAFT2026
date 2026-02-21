import 'package:mongo_dart/mongo_dart.dart';

/// User Model
/// Represents a user in the Dot Dev Club system
class UserModel {
  final ObjectId? id;
  final String uid; // Firebase Auth UID
  final String email;
  final String name;
  final String registrationNumber;
  final String phoneNumber;
  final String role; // admin, team_leader, member
  final String? teamId;
  final String? profilePhotoUrl;
  final DateTime createdAt;
  final DateTime updatedAt;

  UserModel({
    this.id,
    required this.uid,
    required this.email,
    required this.name,
    required this.registrationNumber,
    required this.phoneNumber,
    required this.role,
    this.teamId,
    this.profilePhotoUrl,
    DateTime? createdAt,
    DateTime? updatedAt,
  })  : createdAt = createdAt ?? DateTime.now(),
        updatedAt = updatedAt ?? DateTime.now();

  // Convert to Map for MongoDB
  Map<String, dynamic> toMap() {
    return {
      if (id != null) '_id': id,
      'uid': uid,
      'email': email,
      'name': name,
      'registrationNumber': registrationNumber,
      'phoneNumber': phoneNumber,
      'role': role,
      'teamId': teamId,
      'profilePhotoUrl': profilePhotoUrl,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt.toIso8601String(),
    };
  }

  // Create from Map
  factory UserModel.fromMap(Map<String, dynamic> map) {
    return UserModel(
      id: map['_id'] as ObjectId?,
      uid: map['uid'] as String,
      email: map['email'] as String,
      name: map['name'] as String,
      registrationNumber: map['registrationNumber'] as String,
      phoneNumber: map['phoneNumber'] as String,
      role: map['role'] as String,
      teamId: map['teamId'] as String?,
      profilePhotoUrl: map['profilePhotoUrl'] as String?,
      createdAt: DateTime.parse(map['createdAt'] as String),
      updatedAt: DateTime.parse(map['updatedAt'] as String),
    );
  }

  // Copy with method for updates
  UserModel copyWith({
    ObjectId? id,
    String? uid,
    String? email,
    String? name,
    String? registrationNumber,
    String? phoneNumber,
    String? role,
    String? teamId,
    String? profilePhotoUrl,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return UserModel(
      id: id ?? this.id,
      uid: uid ?? this.uid,
      email: email ?? this.email,
      name: name ?? this.name,
      registrationNumber: registrationNumber ?? this.registrationNumber,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      role: role ?? this.role,
      teamId: teamId ?? this.teamId,
      profilePhotoUrl: profilePhotoUrl ?? this.profilePhotoUrl,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? DateTime.now(),
    );
  }

  bool get isAdmin => role == 'admin';
  bool get isTeamLeader => role == 'team_leader';
  bool get isMember => role == 'member';
}
