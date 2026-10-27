import 'package:flutter/material.dart';

class WorldLogo extends StatelessWidget {
  final double size;
  const WorldLogo({super.key, this.size = 100});
  @override
  Widget build(BuildContext context) => CustomPaint(size: Size(size, size), painter: _LogoPainter());
}

class _LogoPainter extends CustomPainter {
  @override
  void paint(Canvas c, Size s) {
    final r = s.width / 2;
    final ctr = Offset(r, r);
    c.drawCircle(ctr, r, Paint()..color = const Color(0xFF17338A));
    final line = Paint()
      ..color = const Color(0xFF9FB0E0)
      ..style = PaintingStyle.stroke
      ..strokeWidth = s.width * 0.02;
    for (final dy in [-0.28, 0.0, 0.28]) {
      final y = r + dy * r * 1.2;
      c.drawLine(Offset(r * 0.15, y), Offset(r * 1.85, y), line);
    }
    c.drawOval(Rect.fromCenter(center: ctr, width: r * 0.8, height: r * 2), line..strokeWidth = s.width * 0.025);
    final arc = Path()
      ..moveTo(r * 0.55, r * 1.35)
      ..quadraticBezierTo(r * 1.0, r * 0.7, r * 1.45, r * 0.8);
    c.drawPath(arc, Paint()
      ..color = const Color(0xFFFF7A1A)
      ..style = PaintingStyle.stroke
      ..strokeWidth = s.width * 0.05
      ..strokeCap = StrokeCap.round);
    for (final o in [Offset(r * 0.55, r * 1.35), Offset(r * 1.45, r * 0.8)]) {
      c.drawCircle(o, s.width * 0.085, Paint()..color = const Color(0xFFFF7A1A));
      c.drawCircle(o, s.width * 0.05, Paint()..color = Colors.white);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter old) => false;
}
