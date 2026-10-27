import 'package:flutter/material.dart';

class WL {
  static const blue = Color(0xFF1E6FFF);
  static const navy = Color(0xFF0B1646);
  static const night = Color(0xFF070D24);
  static const orange = Color(0xFFFF7A1A);
  static const red = Color(0xFFE5233B);
}

ThemeData buildTheme(Brightness b) {
  final dark = b == Brightness.dark;
  final scheme = ColorScheme.fromSeed(
    seedColor: WL.blue,
    brightness: b,
    primary: dark ? const Color(0xFF6EA8FF) : WL.blue,
    secondary: WL.orange,
    surface: dark ? WL.night : Colors.white,
  );
  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    scaffoldBackgroundColor: dark ? WL.night : Colors.white,
    appBarTheme: AppBarTheme(
      backgroundColor: dark ? WL.night : Colors.white,
      foregroundColor: dark ? Colors.white : WL.navy,
      elevation: 0,
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: WL.orange,
        foregroundColor: Colors.black,
        minimumSize: const Size.fromHeight(48),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
    ),
  );
}
