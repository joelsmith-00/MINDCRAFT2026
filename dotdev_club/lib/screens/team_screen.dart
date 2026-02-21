import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/team_model.dart';
import '../models/user_model.dart';
import '../providers/user_provider.dart';
import '../services/database_service.dart';
import '../utils/theme.dart';

class TeamScreen extends StatefulWidget {
  const TeamScreen({super.key});

  @override
  State<TeamScreen> createState() => _TeamScreenState();
}

class _TeamScreenState extends State<TeamScreen> {
  final _dbService = DatabaseService();

  @override
  Widget build(BuildContext context) {
    final userProvider = Provider.of<UserProvider>(context);
    final user = userProvider.user!;

    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [AppTheme.darkBg, AppTheme.surfaceBg],
        ),
      ),
      child: user.role == UserRole.teamLeader
          ? _buildTeamLeaderView(user)
          : _buildMemberView(user),
    );
  }

  Widget _buildTeamLeaderView(UserModel user) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(20),
          child: Row(
            children: [
              const Expanded(
                child: Text(
                  'My Team',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ),
              if (user.teamId == null)
                FloatingActionButton(
                  heroTag: 'create_team',
                  onPressed: () => _showCreateTeamDialog(context, user),
                  child: const Icon(Icons.add),
                ),
            ],
          ),
        ),
        Expanded(
          child: user.teamId != null
              ? _buildTeamContent(user.teamId!)
              : _buildNoTeamView(),
        ),
      ],
    );
  }

  Widget _buildMemberView(UserModel user) {
    if (user.teamId != null) {
      return _buildTeamContent(user.teamId!);
    }

    return Column(
      children: [
        const Padding(
          padding: EdgeInsets.all(20),
          child: Text(
            'Join a Team',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
        ),
        Expanded(
          child: StreamBuilder<List<TeamModel>>(
            stream: _dbService.getTeams(),
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator());
              }

              if (!snapshot.hasData || snapshot.data!.isEmpty) {
                return Center(
                  child: Text(
                    'No teams available',
                    style: TextStyle(
                      fontSize: 18,
                      color: Colors.white.withOpacity(0.5),
                    ),
                  ),
                );
              }

              final teams = snapshot.data!;
              return ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                itemCount: teams.length,
                itemBuilder: (context, index) {
                  return _buildTeamCard(teams[index], user);
                },
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _buildNoTeamView() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.group_add,
            size: 80,
            color: Colors.white.withOpacity(0.3),
          ),
          const SizedBox(height: 16),
          Text(
            'No team created yet',
            style: TextStyle(
              fontSize: 18,
              color: Colors.white.withOpacity(0.5),
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Tap + to create your team',
            style: TextStyle(
              fontSize: 14,
              color: Colors.white.withOpacity(0.3),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTeamContent(String teamId) {
    return Column(
      children: [
        // Team Members
        Expanded(
          child: StreamBuilder<List<UserModel>>(
            stream: _dbService.getTeamMembers(teamId),
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator());
              }

              if (!snapshot.hasData || snapshot.data!.isEmpty) {
                return Center(
                  child: Text(
                    'No team members yet',
                    style: TextStyle(
                      fontSize: 18,
                      color: Colors.white.withOpacity(0.5),
                    ),
                  ),
                );
              }

              final members = snapshot.data!;
              return ListView.builder(
                padding: const EdgeInsets.all(20),
                itemCount: members.length,
                itemBuilder: (context, index) {
                  return _buildMemberCard(members[index]);
                },
              );
            },
          ),
        ),
        
        // Join Requests (for team leaders)
        Consumer<UserProvider>(
          builder: (context, userProvider, _) {
            if (userProvider.isTeamLeader) {
              return _buildJoinRequestsSection(userProvider.user!.uid);
            }
            return const SizedBox.shrink();
          },
        ),
      ],
    );
  }

  Widget _buildMemberCard(UserModel member) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.cardBg,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppTheme.primaryColor.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 25,
            backgroundColor: AppTheme.primaryColor,
            child: Text(
              member.name[0].toUpperCase(),
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  member.name,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  member.email,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.white.withOpacity(0.7),
                  ),
                ),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: member.role == UserRole.teamLeader
                  ? AppTheme.accentColor.withOpacity(0.2)
                  : AppTheme.secondaryColor.withOpacity(0.2),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              member.role.toString().split('.').last.toUpperCase(),
              style: TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.bold,
                color: member.role == UserRole.teamLeader
                    ? AppTheme.accentColor
                    : AppTheme.secondaryColor,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTeamCard(TeamModel team, UserModel user) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.cardBg,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: AppTheme.primaryColor.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      team.name,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Led by ${team.leaderName}',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.white.withOpacity(0.7),
                      ),
                    ),
                  ],
                ),
              ),
              ElevatedButton(
                onPressed: () => _requestToJoinTeam(team, user),
                child: const Text('Join'),
              ),
            ],
          ),
          if (team.description != null) ...[
            const SizedBox(height: 12),
            Text(
              team.description!,
              style: TextStyle(
                fontSize: 14,
                color: Colors.white.withOpacity(0.8),
              ),
            ),
          ],
          const SizedBox(height: 12),
          Row(
            children: [
              Icon(Icons.people, size: 16, color: AppTheme.secondaryColor),
              const SizedBox(width: 6),
              Text(
                '${team.memberIds.length} members',
                style: TextStyle(
                  fontSize: 14,
                  color: AppTheme.secondaryColor,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildJoinRequestsSection(String teamLeaderId) {
    return StreamBuilder<List<JoinRequest>>(
      stream: _dbService.getJoinRequests(teamLeaderId: teamLeaderId),
      builder: (context, snapshot) {
        if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return const SizedBox.shrink();
        }

        final requests = snapshot.data!;
        return Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: AppTheme.cardBg,
            borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Join Requests',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 12),
              ...requests.map((request) => _buildRequestCard(request)).toList(),
            ],
          ),
        );
      },
    );
  }

  Widget _buildRequestCard(JoinRequest request) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.surfaceBg,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          Expanded(
            child: Text(
              request.userName,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
          ),
          IconButton(
            onPressed: () => _dbService.approveJoinRequest(
              request.id,
              request.userId,
              request.teamId,
            ),
            icon: const Icon(Icons.check, color: AppTheme.secondaryColor),
          ),
          IconButton(
            onPressed: () => _dbService.rejectJoinRequest(request.id),
            icon: const Icon(Icons.close, color: AppTheme.accentColor),
          ),
        ],
      ),
    );
  }

  void _showCreateTeamDialog(BuildContext context, UserModel user) {
    final nameController = TextEditingController();
    final descController = TextEditingController();

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: AppTheme.cardBg,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Text('Create Team', style: TextStyle(color: Colors.white)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: nameController,
              decoration: const InputDecoration(
                labelText: 'Team Name',
                prefixIcon: Icon(Icons.group),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: descController,
              decoration: const InputDecoration(
                labelText: 'Description',
                prefixIcon: Icon(Icons.description),
              ),
              maxLines: 3,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              if (nameController.text.isEmpty) return;

              final team = TeamModel(
                id: '',
                name: nameController.text,
                leaderId: user.uid,
                leaderName: user.name,
                memberIds: [user.uid],
                createdAt: DateTime.now(),
                description: descController.text,
              );

              String teamId = await _dbService.createTeam(team);
              
              // Update user
              await Provider.of<UserProvider>(context, listen: false).updateUser({
                'teamId': teamId,
                'teamName': nameController.text,
              });

              if (context.mounted) {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Team created successfully!')),
                );
              }
            },
            child: const Text('Create'),
          ),
        ],
      ),
    );
  }

  void _requestToJoinTeam(TeamModel team, UserModel user) async {
    final request = JoinRequest(
      id: '',
      userId: user.uid,
      userName: user.name,
      teamId: team.id,
      teamName: team.name,
      teamLeaderId: team.leaderId,
      requestedAt: DateTime.now(),
      status: 'pending',
    );

    await _dbService.createJoinRequest(request);

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Join request sent!')),
      );
    }
  }
}
