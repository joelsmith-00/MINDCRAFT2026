import 'package:flutter/material.dart';
import 'dart:async';
import 'package:flutter_animate/flutter_animate.dart';
import '../config/app_theme.dart';
import '../services/auth_service.dart';
import '../utils/animation_utils.dart';
import 'auth/login_screen.dart';
import 'home/home_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _navigateToNextScreen();
  }

  Future<void> _navigateToNextScreen() async {
    await Future.delayed(const Duration(milliseconds: 3500));
    
    if (!mounted) return;

    // Check if user is already signed in
    final isSignedIn = AuthService.instance.isSignedIn;
    
    Navigator.of(context).pushReplacement(
      PageRouteBuilder(
        pageBuilder: (context, animation, secondaryAnimation) =>
            isSignedIn ? const HomeScreen() : const LoginScreen(),
        transitionsBuilder: (context, animation, secondaryAnimation, child) {
          return FadeTransition(
            opacity: animation,
            child: SlideTransition(
              position: Tween<Offset>(
                begin: const Offset(0.1, 0),
                end: Offset.zero,
              ).animate(CurvedAnimation(
                parent: animation,
                curve: Curves.easeOut,
              )),
              child: child,
            ),
          );
        },
        transitionDuration: const Duration(milliseconds: 600),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              AppTheme.darkBackground,
              Color(0xFF1A1F3A),
              AppTheme.darkBackground,
            ],
          ),
        ),
        child: Stack(
          children: [
            // Animated background circles with stagger
            ...List.generate(3, (index) {
              return Positioned(
                top: -100 + (index * 200.0),
                right: -100 + (index * 150.0),
                child: Container(
                  width: 300,
                  height: 300,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: RadialGradient(
                      colors: [
                        AppTheme.primaryCyan.withOpacity(0.1),
                        AppTheme.primaryPurple.withOpacity(0.05),
                        Colors.transparent,
                      ],
                    ),
                  ),
                )
                    .animate()
                    .fadeIn(
                      duration: AnimationUtils.slower,
                      delay: AnimationUtils.staggerDelay(index),
                    )
                    .scale(
                      duration: AnimationUtils.slower,
                      delay: AnimationUtils.staggerDelay(index),
                      curve: Curves.elasticOut,
                    ),
              );
            }),
            
            // Main content
            Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Logo with scale and fade animation
                  Container(
                    width: 200,
                    height: 200,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(30),
                      gradient: AppTheme.primaryGradient,
                      boxShadow: [
                        BoxShadow(
                          color: AppTheme.primaryCyan.withOpacity(0.3),
                          blurRadius: 30,
                          spreadRadius: 5,
                        ),
                      ],
                    ),
                    child: Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          // Dot text with slide in from left
                          Text(
                            'dot',
                            style: TextStyle(
                              fontSize: 48,
                              fontWeight: FontWeight.w900,
                              color: Colors.white,
                              fontFamily: 'monospace',
                              letterSpacing: 2,
                            ),
                          )
                              .animate()
                              .fadeIn(
                                duration: AnimationUtils.normal,
                                delay: 400.ms,
                              )
                              .slideX(
                                begin: -0.5,
                                duration: AnimationUtils.slow,
                                delay: 400.ms,
                                curve: Curves.elasticOut,
                              ),
                          
                          // .DEV text with slide in from right
                          ShaderMask(
                            shaderCallback: (bounds) => LinearGradient(
                              colors: [
                                AppTheme.primaryCyan,
                                AppTheme.primaryPurple,
                              ],
                            ).createShader(bounds),
                            child: Text(
                              '.DEV',
                              style: TextStyle(
                                fontSize: 36,
                                fontWeight: FontWeight.w900,
                                color: Colors.white,
                                letterSpacing: 3,
                              ),
                            ),
                          )
                              .animate()
                              .fadeIn(
                                duration: AnimationUtils.normal,
                                delay: 600.ms,
                              )
                              .slideX(
                                begin: 0.5,
                                duration: AnimationUtils.slow,
                                delay: 600.ms,
                                curve: Curves.elasticOut,
                              ),
                        ],
                      ),
                    ),
                  )
                      .animate()
                      .fadeIn(duration: AnimationUtils.slow)
                      .scale(
                        duration: AnimationUtils.slower,
                        curve: Curves.elasticOut,
                        begin: const Offset(0.5, 0.5),
                      )
                      .shimmer(
                        duration: 2000.ms,
                        delay: 1000.ms,
                        color: Colors.white.withOpacity(0.3),
                      ),
                  
                  const SizedBox(height: 40),
                  
                  // App subtitle with fade in from bottom
                  Text(
                    'Club Management',
                    style: AppTheme.heading3.copyWith(
                      color: AppTheme.textSecondary,
                    ),
                  )
                      .animate()
                      .fadeIn(
                        duration: AnimationUtils.normal,
                        delay: 1200.ms,
                      )
                      .slideY(
                        begin: 0.3,
                        duration: AnimationUtils.slow,
                        delay: 1200.ms,
                        curve: Curves.easeOut,
                      ),
                  
                  const SizedBox(height: 60),
                  
                  // Loading indicator with scale animation
                  SizedBox(
                    width: 40,
                    height: 40,
                    child: CircularProgressIndicator(
                      strokeWidth: 3,
                      valueColor: AlwaysStoppedAnimation<Color>(
                        AppTheme.primaryCyan,
                      ),
                    ),
                  )
                      .animate()
                      .fadeIn(
                        duration: AnimationUtils.normal,
                        delay: 1500.ms,
                      )
                      .scale(
                        duration: AnimationUtils.slow,
                        delay: 1500.ms,
                        curve: Curves.elasticOut,
                      ),
                ],
              ),
            ),
            
            // Version info at bottom with fade in
            Positioned(
              bottom: 40,
              left: 0,
              right: 0,
              child: Text(
                'Version 1.0.0',
                textAlign: TextAlign.center,
                style: AppTheme.caption,
              )
                  .animate()
                  .fadeIn(
                    duration: AnimationUtils.normal,
                    delay: 2000.ms,
                  )
                  .slideY(
                    begin: 0.5,
                    duration: AnimationUtils.slow,
                    delay: 2000.ms,
                  ),
            ),
          ],
        ),
      ),
    );
  }
}

