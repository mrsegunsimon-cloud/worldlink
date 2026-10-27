import 'dart:async';
import 'package:flutter/material.dart';
import 'theme.dart';
import 'pages/feed_page.dart';
import 'pages/explore_page.dart';
import 'pages/music_page.dart';
import 'pages/simple_pages.dart';
import 'pages/sos.dart';
import 'pages/logo.dart';

void main() => runApp(const WorldLinkApp());

class WorldLinkApp extends StatelessWidget {
  const WorldLinkApp({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'WorldLink',
        debugShowCheckedModeBanner: false,
        theme: buildTheme(Brightness.dark),
        darkTheme: buildTheme(Brightness.dark),
        themeMode: ThemeMode.dark,
        home: const Splash(),
      );
}

class Splash extends StatefulWidget {
  const Splash({super.key});
  @override
  State<Splash> createState() => _SplashState();
}

class _SplashState extends State<Splash> {
  @override
  void initState() {
    super.initState();
    Timer(const Duration(milliseconds: 2200), () {
      if (!mounted) return;
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const Shell()));
    });
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        backgroundColor: const Color(0xFF050B24),
        body: Center(
          child: Column(mainAxisSize: MainAxisSize.min, children: const [
            WorldLogo(size: 100),
            SizedBox(height: 16),
            Text('WorldLink', style: TextStyle(color: Colors.white, fontSize: 30, fontWeight: FontWeight.w800)),
            SizedBox(height: 8),
            Text('Connect with the world', style: TextStyle(color: Color(0xFF9AA6C8), fontSize: 16)),
          ]),
        ),
      );
}

class Shell extends StatefulWidget {
  const Shell({super.key});
  @override
  State<Shell> createState() => _ShellState();
}

class _ShellState extends State<Shell> {
  int tab = 0;

  void _push(Widget w) => Navigator.push(context, MaterialPageRoute(builder: (_) => w));

  @override
  Widget build(BuildContext context) {
    final pages = <Widget>[
      FeedPage(active: tab == 0, onMenu: () => _scaffold.currentState?.openDrawer()),
      const FriendsPage(),
      const CreatePage(),
      const InboxPage(),
      const ProfilePage(),
    ];
    return Scaffold(
      key: _scaffold,
      backgroundColor: Colors.black,
      drawer: Drawer(
        backgroundColor: const Color(0xFF0B1230),
        child: SafeArea(
          child: ListView(children: [
            const ListTile(title: Text('WorldLink', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800))),
            ListTile(leading: const Icon(Icons.explore), title: const Text('Explore · World Tourism'), onTap: () { Navigator.pop(context); _push(const ExplorePage()); }),
            ListTile(leading: const Icon(Icons.music_note), title: const Text('Music'), onTap: () { Navigator.pop(context); _push(const MusicPage()); }),
          ]),
        ),
      ),
      body: Stack(children: [
        IndexedStack(index: tab, children: pages),
        Positioned(top: MediaQuery.of(context).padding.top + 52, left: 12, child: const SosButton()),
      ]),
      bottomNavigationBar: Container(
        color: Colors.black,
        child: SafeArea(
          top: false,
          child: SizedBox(
            height: 64,
            child: Row(children: [
              _item(0, Icons.home_outlined, 'Home'),
              _item(1, Icons.sentiment_satisfied_alt_outlined, 'Friends'),
              Expanded(
                child: Center(
                  child: GestureDetector(
                    onTap: () => setState(() => tab = 2),
                    child: Container(
                      width: 56,
                      height: 36,
                      padding: const EdgeInsets.all(2.5),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(11),
                        gradient: const LinearGradient(colors: [WL.blue, WL.orange]),
                      ),
                      child: Container(
                        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(9)),
                        child: const Icon(Icons.add, color: Colors.black, size: 26),
                      ),
                    ),
                  ),
                ),
              ),
              _item(3, Icons.mail_outline, 'Inbox'),
              _item(4, Icons.account_circle_outlined, 'Profile'),
            ]),
          ),
        ),
      ),
    );
  }

  final _scaffold = GlobalKey<ScaffoldState>();

  Widget _item(int i, IconData ic, String label) {
    final on = tab == i;
    final c = on ? Colors.white : const Color(0xFF9A9A9A);
    return Expanded(
      child: InkWell(
        onTap: () => setState(() => tab = i),
        child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          Icon(ic, color: c, size: 26),
          Text(label, style: TextStyle(color: c, fontSize: 12, fontWeight: on ? FontWeight.w700 : FontWeight.w400)),
        ]),
      ),
    );
  }
}
