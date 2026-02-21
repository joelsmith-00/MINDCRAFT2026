import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

/// Animation Utilities
/// Provides Framer Motion-style animation presets and utilities
class AnimationUtils {
  // Duration constants
  static const Duration fast = Duration(milliseconds: 200);
  static const Duration normal = Duration(milliseconds: 300);
  static const Duration slow = Duration(milliseconds: 500);
  static const Duration slower = Duration(milliseconds: 800);

  // Delay constants
  static const Duration delayShort = Duration(milliseconds: 100);
  static const Duration delayMedium = Duration(milliseconds: 200);
  static const Duration delayLong = Duration(milliseconds: 300);

  // Curves
  static const Curve easeOut = Curves.easeOut;
  static const Curve easeIn = Curves.easeIn;
  static const Curve easeInOut = Curves.easeInOut;
  static const Curve spring = Curves.elasticOut;
  static const Curve bounce = Curves.bounceOut;

  /// Fade in from bottom (like Framer Motion's initial={{ y: 20, opacity: 0 }})
  static List<Effect> fadeInUp({
    Duration? delay,
    Duration? duration,
  }) {
    return [
      FadeEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: easeOut,
      ),
      SlideEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: easeOut,
        begin: const Offset(0, 0.3),
        end: Offset.zero,
      ),
    ];
  }

  /// Fade in from top
  static List<Effect> fadeInDown({
    Duration? delay,
    Duration? duration,
  }) {
    return [
      FadeEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: easeOut,
      ),
      SlideEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: easeOut,
        begin: const Offset(0, -0.3),
        end: Offset.zero,
      ),
    ];
  }

  /// Fade in from left
  static List<Effect> fadeInLeft({
    Duration? delay,
    Duration? duration,
  }) {
    return [
      FadeEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: easeOut,
      ),
      SlideEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: easeOut,
        begin: const Offset(-0.3, 0),
        end: Offset.zero,
      ),
    ];
  }

  /// Fade in from right
  static List<Effect> fadeInRight({
    Duration? delay,
    Duration? duration,
  }) {
    return [
      FadeEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: easeOut,
      ),
      SlideEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: easeOut,
        begin: const Offset(0.3, 0),
        end: Offset.zero,
      ),
    ];
  }

  /// Scale in (pop effect)
  static List<Effect> scaleIn({
    Duration? delay,
    Duration? duration,
    double? begin,
  }) {
    return [
      FadeEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: easeOut,
      ),
      ScaleEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: spring,
        begin: Offset(begin ?? 0.8, begin ?? 0.8),
        end: const Offset(1, 1),
      ),
    ];
  }

  /// Shimmer effect for loading states
  static List<Effect> shimmer({
    Duration? duration,
  }) {
    return [
      ShimmerEffect(
        duration: duration ?? const Duration(milliseconds: 1500),
        color: Colors.white.withOpacity(0.3),
      ),
    ];
  }

  /// Stagger children animations
  static Duration staggerDelay(int index, {Duration? baseDelay}) {
    return (baseDelay ?? delayShort) * (index + 1);
  }

  /// Pulse animation (for notifications, badges, etc.)
  static Widget pulse({
    Duration? duration,
    Widget? child,
  }) {
    return Animate(
      effects: [
        ScaleEffect(
          duration: duration ?? const Duration(milliseconds: 1000),
          curve: Curves.easeInOut,
          begin: const Offset(1, 1),
          end: const Offset(1.1, 1.1),
        ),
      ],
      onComplete: (controller) => controller.repeat(reverse: true),
      child: child ?? const SizedBox(),
    );
  }

  /// Rotate in
  static List<Effect> rotateIn({
    Duration? delay,
    Duration? duration,
  }) {
    return [
      FadeEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
      ),
      RotateEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: spring,
        begin: -0.2,
        end: 0,
      ),
    ];
  }

  /// Blur in effect
  static List<Effect> blurIn({
    Duration? delay,
    Duration? duration,
  }) {
    return [
      FadeEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
      ),
      BlurEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        begin: const Offset(10, 10),
        end: Offset.zero,
      ),
    ];
  }

  /// Slide and fade (for page transitions)
  static List<Effect> slideAndFade({
    Duration? delay,
    Duration? duration,
    Offset? begin,
  }) {
    return [
      FadeEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: easeOut,
      ),
      SlideEffect(
        delay: delay ?? Duration.zero,
        duration: duration ?? normal,
        curve: easeOut,
        begin: begin ?? const Offset(0.2, 0),
        end: Offset.zero,
      ),
    ];
  }
}

/// Extension to easily apply animations to widgets
extension AnimateExtensions on Widget {
  Widget fadeInUp({Duration? delay, Duration? duration}) {
    return animate(effects: AnimationUtils.fadeInUp(delay: delay, duration: duration));
  }

  Widget fadeInDown({Duration? delay, Duration? duration}) {
    return animate(effects: AnimationUtils.fadeInDown(delay: delay, duration: duration));
  }

  Widget fadeInLeft({Duration? delay, Duration? duration}) {
    return animate(effects: AnimationUtils.fadeInLeft(delay: delay, duration: duration));
  }

  Widget fadeInRight({Duration? delay, Duration? duration}) {
    return animate(effects: AnimationUtils.fadeInRight(delay: delay, duration: duration));
  }

  Widget scaleIn({Duration? delay, Duration? duration, double? begin}) {
    return animate(effects: AnimationUtils.scaleIn(delay: delay, duration: duration, begin: begin));
  }

  Widget shimmer({Duration? duration}) {
    return animate(effects: AnimationUtils.shimmer(duration: duration));
  }

  Widget rotateIn({Duration? delay, Duration? duration}) {
    return animate(effects: AnimationUtils.rotateIn(delay: delay, duration: duration));
  }

  Widget blurIn({Duration? delay, Duration? duration}) {
    return animate(effects: AnimationUtils.blurIn(delay: delay, duration: duration));
  }

  Widget slideAndFade({Duration? delay, Duration? duration, Offset? begin}) {
    return animate(effects: AnimationUtils.slideAndFade(delay: delay, duration: duration, begin: begin));
  }
}
