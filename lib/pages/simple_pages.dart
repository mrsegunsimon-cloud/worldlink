import 'package:flutter/material.dart';
import '../theme.dart';

class _Soon extends StatelessWidget {
  final String title, text;
  final IconData icon;
  const _Soon(this.title, this.text, this.icon);
  @override
  Widget build(BuildContext context) => SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(28),
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              Icon(icon, size: 64, color: WL.blue),
              const SizedBox(height: 14),
              Text(title, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
              const SizedBox(height: 8),
              Text(text, textAlign: TextAlign.center),
            ]),
          ),
        ),
      );
}

class CreatePage extends StatelessWidget {
  const CreatePage({super.key});
  @override
  Widget build(BuildContext context) => const _Soon('Create', 'Camera, face effects and voice effects arrive in the next build.', Icons.videocam);
}

class InboxPage extends StatelessWidget {
  const InboxPage({super.key});
  @override
  Widget build(BuildContext context) => const _Soon('Inbox', 'Messages and video calls arrive after sign-in is added.', Icons.chat);
}

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});
  @override
  Widget build(BuildContext context) => const _Soon('Profile', 'Sign up and log in come next.', Icons.person);
}
