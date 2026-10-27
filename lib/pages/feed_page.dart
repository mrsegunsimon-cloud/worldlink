import 'package:flutter/material.dart';
import '../theme.dart';
import '../data.dart';

class Post {
  final String emoji, user, caption, sound;
  final String likes, gifts;
  final Color top, bottom;
  const Post(this.emoji, this.user, this.caption, this.sound, this.likes, this.gifts, this.top, this.bottom);
}

const posts = <Post>[
  Post('🍋', '@maya.ortiz', 'Free lemons on the porch today #neighbors', 'Original sound - maya.ortiz', '1.2K', '155', Color(0xFFFFB347), Color(0xFF4A2308)),
  Post('🌍', '@sam.lee', 'Saturday street cleanup, who is in? #community', 'Original sound - sam.lee', '8.3K', '1K', Color(0xFF4FC3A1), Color(0xFF082E30)),
  Post('⚽', '@goalhub', 'What a finish! #football', 'Stadium roar - goalhub', '52K', '6.5K', Color(0xFF4CAF50), Color(0xFF0D2A12)),
  Post('📚', '@campus.daily', 'Study group tips that actually work #campus', 'Lo-fi beats - campus.daily', '910', '113', Color(0xFF8E6BD0), Color(0xFF1B1038)),
  Post('🎧', '@dj.kemi', 'New beat dropping Friday #music', 'Friday - dj.kemi', '23K', '2.9K', Color(0xFFEC5C93), Color(0xFF33102A)),
];

class FeedPage extends StatefulWidget {
  final bool active;
  final VoidCallback onMenu;
  const FeedPage({super.key, required this.active, required this.onMenu});
  @override
  State<FeedPage> createState() => _FeedPageState();
}

class _FeedPageState extends State<FeedPage> {
  int _top = 2;

  @override
  Widget build(BuildContext context) {
    final pad = MediaQuery.of(context).padding.top;
    return Stack(children: [
      PageView.builder(
        scrollDirection: Axis.vertical,
        itemCount: posts.length,
        itemBuilder: (_, i) => PostView(post: posts[i]),
      ),
      Positioned(
        top: pad + 6,
        left: 8,
        right: 8,
        child: Row(children: [
          IconButton(icon: const Icon(Icons.menu, color: Colors.white, size: 28), onPressed: widget.onMenu),
          Expanded(
            child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
              for (final e in ['Community', 'Following', 'For You'].asMap().entries)
                GestureDetector(
                  onTap: () => setState(() => _top = e.key),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 9),
                    child: Container(
                      padding: const EdgeInsets.only(bottom: 3),
                      decoration: BoxDecoration(
                        border: Border(bottom: BorderSide(color: _top == e.key ? Colors.white : Colors.transparent, width: 2)),
                      ),
                      child: Text(e.value,
                          style: TextStyle(
                            color: _top == e.key ? Colors.white : Colors.white70,
                            fontWeight: FontWeight.w700,
                            fontSize: 16,
                          )),
                    ),
                  ),
                ),
            ]),
          ),
          const Icon(Icons.notifications, color: Color(0xFFFFD54F), size: 26),
          const SizedBox(width: 10),
          const Icon(Icons.search, color: Colors.white, size: 28),
          const SizedBox(width: 8),
        ]),
      ),
    ]);
  }
}

class PostView extends StatefulWidget {
  final Post post;
  const PostView({super.key, required this.post});
  @override
  State<PostView> createState() => _PostViewState();
}

class _PostViewState extends State<PostView> {
  bool liked = false, saved = false;

  void _gifts() => showModalBottomSheet(
        context: context,
        backgroundColor: const Color(0xFF111833),
        builder: (_) => SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Wrap(spacing: 12, runSpacing: 12, children: [
              for (final g in gifts)
                InkWell(
                  onTap: () {
                    Navigator.pop(context);
                    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('${g[0]} ${g[1]} sent (demo)')));
                  },
                  child: SizedBox(
                    width: 76,
                    child: Column(children: [
                      Text(g[0] as String, style: const TextStyle(fontSize: 32)),
                      Text(g[1] as String),
                      Text('${g[2]} coins', style: const TextStyle(fontSize: 11)),
                    ]),
                  ),
                ),
            ]),
          ),
        ),
      );

  Widget _rail(Widget icon, String label, VoidCallback f) => Padding(
        padding: const EdgeInsets.only(bottom: 14),
        child: InkWell(
          onTap: f,
          child: Column(children: [
            icon,
            const SizedBox(height: 2),
            Text(label, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w700)),
          ]),
        ),
      );

  @override
  Widget build(BuildContext context) {
    final p = widget.post;
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [p.top, p.bottom]),
      ),
      child: Stack(fit: StackFit.expand, children: [
        Center(child: Text(p.emoji, style: const TextStyle(fontSize: 120))),
        Positioned(
          right: 10,
          bottom: 28,
          child: Column(children: [
            Container(
              width: 50,
              height: 50,
              margin: const EdgeInsets.only(bottom: 16),
              decoration: BoxDecoration(
                color: const Color(0xFF1B2330),
                shape: BoxShape.circle,
                border: Border.all(color: const Color(0xFF29B6F6), width: 3),
              ),
              alignment: Alignment.center,
              child: Text(p.user.substring(1, 2).toUpperCase(), style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 18)),
            ),
            _rail(Icon(liked ? Icons.favorite : Icons.favorite, color: liked ? WL.red : Colors.white, size: 36), p.likes, () => setState(() => liked = !liked)),
            _rail(const Icon(Icons.chat_bubble, color: Colors.white, size: 34), '2', () {}),
            _rail(const Text('🎁', style: TextStyle(fontSize: 34)), 'Gift', _gifts),
            _rail(Icon(Icons.bookmark, color: saved ? WL.orange : Colors.white, size: 34), p.gifts, () => setState(() => saved = !saved)),
            _rail(const Icon(Icons.north_east, color: Colors.white, size: 32), 'Share', () {}),
            _rail(const Icon(Icons.more_horiz, color: Colors.white, size: 34), 'More', () {}),
            Container(
              width: 40,
              height: 40,
              decoration: const BoxDecoration(color: Color(0xFF111111), shape: BoxShape.circle),
              child: const Icon(Icons.music_note, color: Colors.white, size: 18),
            ),
          ]),
        ),
        Positioned(
          left: 14,
          right: 84,
          bottom: 26,
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisSize: MainAxisSize.min, children: [
            Text(p.user, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 18)),
            const SizedBox(height: 6),
            Text(p.caption, style: const TextStyle(color: Colors.white, fontSize: 17, height: 1.25)),
            const SizedBox(height: 6),
            const Text('Translate', style: TextStyle(color: Colors.white, fontSize: 13, decoration: TextDecoration.underline)),
            const SizedBox(height: 14),
            Text('♪ ${p.sound}', style: const TextStyle(color: Colors.white, fontSize: 14)),
          ]),
        ),
      ]),
    );
  }
}
