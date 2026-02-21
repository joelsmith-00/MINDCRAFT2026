import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:async';
import 'dart:math';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  runApp(const SpaceShooterApp());
}

class SpaceShooterApp extends StatelessWidget {
  const SpaceShooterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Space Shooter',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.blue,
        fontFamily: 'Courier',
      ),
      home: const MenuScreen(),
    );
  }
}

class MenuScreen extends StatelessWidget {
  const MenuScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Color(0xFF0A0E27),
              Color(0xFF1A1F3A),
              Color(0xFF2D1B4E),
            ],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Title with glow effect
                Container(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    children: [
                      Text(
                        '🚀',
                        style: TextStyle(fontSize: 80),
                      ),
                      const SizedBox(height: 20),
                      ShaderMask(
                        shaderCallback: (bounds) => const LinearGradient(
                          colors: [Color(0xFF00F5FF), Color(0xFF0080FF)],
                        ).createShader(bounds),
                        child: const Text(
                          'SPACE SHOOTER',
                          style: TextStyle(
                            fontSize: 48,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                            letterSpacing: 4,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 60),
                // Play Button
                GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const GameScreen(),
                      ),
                    );
                  },
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 60,
                      vertical: 20,
                    ),
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [Color(0xFF00F5FF), Color(0xFF0080FF)],
                      ),
                      borderRadius: BorderRadius.circular(30),
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0xFF00F5FF).withOpacity(0.5),
                          blurRadius: 20,
                          spreadRadius: 2,
                        ),
                      ],
                    ),
                    child: const Text(
                      'START GAME',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                        letterSpacing: 2,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 40),
                // Instructions
                Container(
                  margin: const EdgeInsets.symmetric(horizontal: 40),
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(15),
                    border: Border.all(
                      color: Colors.white.withOpacity(0.2),
                      width: 1,
                    ),
                  ),
                  child: const Column(
                    children: [
                      Text(
                        'HOW TO PLAY',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF00F5FF),
                        ),
                      ),
                      SizedBox(height: 10),
                      Text(
                        '• Drag to move your ship\n• Avoid enemies\n• Shoot them down\n• Survive as long as you can!',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.white70,
                          height: 1.5,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class GameScreen extends StatefulWidget {
  const GameScreen({super.key});

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> with TickerProviderStateMixin {
  // Game state
  double playerX = 0.5;
  double playerY = 0.8;
  int score = 0;
  int health = 3;
  bool gameOver = false;
  bool isPaused = false;

  // Game objects
  List<Bullet> bullets = [];
  List<Enemy> enemies = [];
  List<Particle> particles = [];
  List<Star> stars = [];

  // Timers
  Timer? gameLoop;
  Timer? enemySpawner;
  Timer? shootTimer;

  // Random
  final Random random = Random();

  @override
  void initState() {
    super.initState();
    initStars();
    startGame();
  }

  void initStars() {
    for (int i = 0; i < 100; i++) {
      stars.add(Star(
        x: random.nextDouble(),
        y: random.nextDouble(),
        speed: 0.001 + random.nextDouble() * 0.003,
        size: 1 + random.nextDouble() * 2,
      ));
    }
  }

  void startGame() {
    // Main game loop (60 FPS)
    gameLoop = Timer.periodic(const Duration(milliseconds: 16), (timer) {
      if (!isPaused && !gameOver) {
        updateGame();
      }
    });

    // Enemy spawner
    enemySpawner = Timer.periodic(const Duration(milliseconds: 1500), (timer) {
      if (!isPaused && !gameOver) {
        spawnEnemy();
      }
    });

    // Auto shoot
    shootTimer = Timer.periodic(const Duration(milliseconds: 300), (timer) {
      if (!isPaused && !gameOver) {
        shoot();
      }
    });
  }

  void updateGame() {
    setState(() {
      // Update stars
      for (var star in stars) {
        star.y += star.speed;
        if (star.y > 1) {
          star.y = 0;
          star.x = random.nextDouble();
        }
      }

      // Update bullets
      bullets.removeWhere((bullet) {
        bullet.y -= 0.02;
        return bullet.y < 0;
      });

      // Update enemies
      enemies.removeWhere((enemy) {
        enemy.y += enemy.speed;
        return enemy.y > 1;
      });

      // Update particles
      particles.removeWhere((particle) {
        particle.update();
        return particle.life <= 0;
      });

      // Check collisions
      checkCollisions();
    });
  }

  void spawnEnemy() {
    enemies.add(Enemy(
      x: 0.1 + random.nextDouble() * 0.8,
      y: -0.05,
      speed: 0.003 + random.nextDouble() * 0.005,
      type: random.nextInt(3),
    ));
  }

  void shoot() {
    bullets.add(Bullet(x: playerX, y: playerY - 0.05));
  }

  void checkCollisions() {
    // Bullet-Enemy collisions
    for (int i = bullets.length - 1; i >= 0; i--) {
      for (int j = enemies.length - 1; j >= 0; j--) {
        if ((bullets[i].x - enemies[j].x).abs() < 0.05 &&
            (bullets[i].y - enemies[j].y).abs() < 0.05) {
          // Hit!
          createExplosion(enemies[j].x, enemies[j].y);
          bullets.removeAt(i);
          enemies.removeAt(j);
          score += 10;
          break;
        }
      }
    }

    // Player-Enemy collisions
    for (int i = enemies.length - 1; i >= 0; i--) {
      if ((playerX - enemies[i].x).abs() < 0.06 &&
          (playerY - enemies[i].y).abs() < 0.06) {
        createExplosion(enemies[i].x, enemies[i].y);
        enemies.removeAt(i);
        health--;
        if (health <= 0) {
          endGame();
        }
      }
    }
  }

  void createExplosion(double x, double y) {
    for (int i = 0; i < 20; i++) {
      particles.add(Particle(
        x: x,
        y: y,
        vx: (random.nextDouble() - 0.5) * 0.01,
        vy: (random.nextDouble() - 0.5) * 0.01,
      ));
    }
  }

  void endGame() {
    setState(() {
      gameOver = true;
    });
    gameLoop?.cancel();
    enemySpawner?.cancel();
    shootTimer?.cancel();
  }

  void restartGame() {
    setState(() {
      playerX = 0.5;
      playerY = 0.8;
      score = 0;
      health = 3;
      gameOver = false;
      isPaused = false;
      bullets.clear();
      enemies.clear();
      particles.clear();
    });
    startGame();
  }

  @override
  void dispose() {
    gameLoop?.cancel();
    enemySpawner?.cancel();
    shootTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      body: GestureDetector(
        onPanUpdate: (details) {
          if (!gameOver && !isPaused) {
            setState(() {
              playerX = (details.localPosition.dx / size.width).clamp(0.05, 0.95);
              playerY = (details.localPosition.dy / size.height).clamp(0.1, 0.9);
            });
          }
        },
        child: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                Color(0xFF0A0E27),
                Color(0xFF1A1F3A),
                Color(0xFF2D1B4E),
              ],
            ),
          ),
          child: Stack(
            children: [
              // Stars
              ...stars.map((star) => Positioned(
                    left: star.x * size.width,
                    top: star.y * size.height,
                    child: Container(
                      width: star.size,
                      height: star.size,
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.8),
                        shape: BoxShape.circle,
                      ),
                    ),
                  )),

              // Bullets
              ...bullets.map((bullet) => Positioned(
                    left: bullet.x * size.width - 2,
                    top: bullet.y * size.height - 10,
                    child: Container(
                      width: 4,
                      height: 20,
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                          colors: [Color(0xFF00F5FF), Color(0xFF0080FF)],
                        ),
                        borderRadius: BorderRadius.circular(2),
                        boxShadow: [
                          BoxShadow(
                            color: const Color(0xFF00F5FF).withOpacity(0.8),
                            blurRadius: 10,
                            spreadRadius: 2,
                          ),
                        ],
                      ),
                    ),
                  )),

              // Enemies
              ...enemies.map((enemy) => Positioned(
                    left: enemy.x * size.width - 20,
                    top: enemy.y * size.height - 20,
                    child: Container(
                      width: 40,
                      height: 40,
                      child: CustomPaint(
                        painter: EnemyPainter(type: enemy.type),
                      ),
                    ),
                  )),

              // Particles
              ...particles.map((particle) => Positioned(
                    left: particle.x * size.width,
                    top: particle.y * size.height,
                    child: Container(
                      width: 4,
                      height: 4,
                      decoration: BoxDecoration(
                        color: Color.lerp(
                          Colors.orange,
                          Colors.red,
                          1 - particle.life / 30,
                        ),
                        shape: BoxShape.circle,
                      ),
                    ),
                  )),

              // Player
              Positioned(
                left: playerX * size.width - 25,
                top: playerY * size.height - 25,
                child: Container(
                  width: 50,
                  height: 50,
                  child: CustomPaint(
                    painter: PlayerPainter(),
                  ),
                ),
              ),

              // UI
              SafeArea(
                child: Column(
                  children: [
                    // Top bar
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          // Score
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 20,
                              vertical: 10,
                            ),
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.5),
                              borderRadius: BorderRadius.circular(20),
                              border: Border.all(
                                color: const Color(0xFF00F5FF).withOpacity(0.5),
                              ),
                            ),
                            child: Text(
                              'SCORE: $score',
                              style: const TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFF00F5FF),
                              ),
                            ),
                          ),
                          // Health
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 20,
                              vertical: 10,
                            ),
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.5),
                              borderRadius: BorderRadius.circular(20),
                              border: Border.all(
                                color: Colors.red.withOpacity(0.5),
                              ),
                            ),
                            child: Row(
                              children: List.generate(
                                3,
                                (index) => Padding(
                                  padding: const EdgeInsets.symmetric(horizontal: 2),
                                  child: Icon(
                                    Icons.favorite,
                                    color: index < health
                                        ? Colors.red
                                        : Colors.grey.withOpacity(0.3),
                                    size: 20,
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              // Game Over overlay
              if (gameOver)
                Container(
                  color: Colors.black.withOpacity(0.8),
                  child: Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text(
                          'GAME OVER',
                          style: TextStyle(
                            fontSize: 48,
                            fontWeight: FontWeight.bold,
                            color: Colors.red,
                            letterSpacing: 4,
                          ),
                        ),
                        const SizedBox(height: 20),
                        Text(
                          'FINAL SCORE: $score',
                          style: const TextStyle(
                            fontSize: 32,
                            color: Color(0xFF00F5FF),
                          ),
                        ),
                        const SizedBox(height: 40),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            GestureDetector(
                              onTap: restartGame,
                              child: Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 40,
                                  vertical: 15,
                                ),
                                decoration: BoxDecoration(
                                  gradient: const LinearGradient(
                                    colors: [Color(0xFF00F5FF), Color(0xFF0080FF)],
                                  ),
                                  borderRadius: BorderRadius.circular(25),
                                ),
                                child: const Text(
                                  'PLAY AGAIN',
                                  style: TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(width: 20),
                            GestureDetector(
                              onTap: () => Navigator.pop(context),
                              child: Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 40,
                                  vertical: 15,
                                ),
                                decoration: BoxDecoration(
                                  color: Colors.white.withOpacity(0.2),
                                  borderRadius: BorderRadius.circular(25),
                                  border: Border.all(color: Colors.white),
                                ),
                                child: const Text(
                                  'MENU',
                                  style: TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}

// Game object classes
class Bullet {
  double x;
  double y;
  Bullet({required this.x, required this.y});
}

class Enemy {
  double x;
  double y;
  double speed;
  int type;
  Enemy({required this.x, required this.y, required this.speed, required this.type});
}

class Particle {
  double x;
  double y;
  double vx;
  double vy;
  int life = 30;

  Particle({required this.x, required this.y, required this.vx, required this.vy});

  void update() {
    x += vx;
    y += vy;
    life--;
  }
}

class Star {
  double x;
  double y;
  double speed;
  double size;
  Star({required this.x, required this.y, required this.speed, required this.size});
}

// Custom painters
class PlayerPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..shader = const LinearGradient(
        colors: [Color(0xFF00F5FF), Color(0xFF0080FF)],
      ).createShader(Rect.fromLTWH(0, 0, size.width, size.height))
      ..style = PaintingStyle.fill;

    final path = Path();
    path.moveTo(size.width / 2, 0);
    path.lineTo(0, size.height);
    path.lineTo(size.width / 2, size.height * 0.8);
    path.lineTo(size.width, size.height);
    path.close();

    canvas.drawPath(path, paint);

    // Glow effect
    final glowPaint = Paint()
      ..color = const Color(0xFF00F5FF).withOpacity(0.3)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 10);
    canvas.drawPath(path, glowPaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

class EnemyPainter extends CustomPainter {
  final int type;
  EnemyPainter({required this.type});

  @override
  void paint(Canvas canvas, Size size) {
    final colors = [
      [Colors.red, Colors.orange],
      [Colors.purple, Colors.pink],
      [Colors.green, Colors.lime],
    ];

    final paint = Paint()
      ..shader = LinearGradient(
        colors: colors[type % 3],
      ).createShader(Rect.fromLTWH(0, 0, size.width, size.height))
      ..style = PaintingStyle.fill;

    if (type == 0) {
      // Triangle enemy
      final path = Path();
      path.moveTo(size.width / 2, size.height);
      path.lineTo(0, 0);
      path.lineTo(size.width, 0);
      path.close();
      canvas.drawPath(path, paint);
    } else if (type == 1) {
      // Circle enemy
      canvas.drawCircle(
        Offset(size.width / 2, size.height / 2),
        size.width / 2,
        paint,
      );
    } else {
      // Square enemy
      canvas.drawRect(
        Rect.fromLTWH(0, 0, size.width, size.height),
        paint,
      );
    }

    // Glow
    final glowPaint = Paint()
      ..color = colors[type % 3][0].withOpacity(0.3)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 8);
    
    if (type == 0) {
      final path = Path();
      path.moveTo(size.width / 2, size.height);
      path.lineTo(0, 0);
      path.lineTo(size.width, 0);
      path.close();
      canvas.drawPath(path, glowPaint);
    } else if (type == 1) {
      canvas.drawCircle(
        Offset(size.width / 2, size.height / 2),
        size.width / 2,
        glowPaint,
      );
    } else {
      canvas.drawRect(
        Rect.fromLTWH(0, 0, size.width, size.height),
        glowPaint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
