import 'package:flutter/material.dart';
import '../models/user_model.dart';
import '../services/auth_service.dart';

class UserProvider extends ChangeNotifier {
  final AuthService _authService = AuthService();
  UserModel? _user;
  bool _isLoading = false;

  UserModel? get user => _user;
  bool get isLoading => _isLoading;
  bool get isAdmin => _user?.role == UserRole.admin;
  bool get isTeamLeader => _user?.role == UserRole.teamLeader;
  bool get isMember => _user?.role == UserRole.member;

  Future<void> loadUser(String uid) async {
    _isLoading = true;
    notifyListeners();

    _user = await _authService.getUserData(uid);

    _isLoading = false;
    notifyListeners();
  }

  void setUser(UserModel user) {
    _user = user;
    notifyListeners();
  }

  void clearUser() {
    _user = null;
    notifyListeners();
  }

  Future<void> updateUser(Map<String, dynamic> data) async {
    if (_user != null) {
      await _authService.updateUserData(_user!.uid, data);
      await loadUser(_user!.uid);
    }
  }
}
