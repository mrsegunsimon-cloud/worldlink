import 'package:flutter/material.dart';
import 'theme.dart';
import 'pages/feed_page.dart';
import 'pages/explore_page.dart';
import 'pages/music_page.dart';
import 'pages/simple_pages.dart';
import 'pages/sos.dart';

void main() => runApp(const WorldLinkApp());

class WorldLinkApp extends StatelessWidget {
  const WorldLinkApp({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'WorldLink',
        debugShowCheckedModeBanner: false,
        theme: buildTheme(Brightness.light),
        darkTheme: buildTheme(Brightness.dark),
        themeMode: ThemeMode.system,
        home: const Shell(),
      );
}

class Shell extends StatefulWidget {
  const Shell({super.key});
  @override
  State<Shell> createState() => _ShellState();
}

class _ShellState extends State<Shell> {
  int tab = 0;

  @override
  Widget build(BuildContext context) {
    final pages = <Widget>[
      FeedPage(active: tab == 0),
      const ExplorePage(),
      const CreatePage(),
      const InboxPage(),
      const ProfilePage(),
    ];
    return Scaffold(
      body: Stack(children: [
        IndexedStack(index: tab, children: pages),
        Positioned(
          top: MediaQuery.of(context).padding.top + 8,
          left: 12,
          child: const SosButton(),
        ),
      ]),
      bottomNavigationBar: NavigationBar(
        selectedIndex: tab,
        onDestinationSelected: (i) => setState(() => tab = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.explore_outlined), selectedIcon: Icon(Icons.explore), label: 'Explore'),
          NavigationDestination(icon: Icon(Icons.add_circle, color: WL.orange, size: 36), label: 'Create'),
          NavigationDestination(icon: Icon(Icons.chat_bubble_outline), selectedIcon: Icon(Icons.chat_bubble), label: 'Inbox'),
          NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}
