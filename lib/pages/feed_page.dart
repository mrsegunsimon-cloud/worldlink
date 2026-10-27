import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import '../data.dart';
import '../theme.dart';

class FeedPage extends StatefulWidget {
  final bool active;
  const FeedPage({super.key, required this.active});
  @override
  State<FeedPage> createState() => _FeedPageState();
}

class _FeedPageState extends State<FeedPage> {
  final _pc = PageController();
  int _cur = 0;
  @override
  void dispose() {
    _pc.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => PageView.builder(
        controller: _pc,
        scrollDirection: Axis.vertical,
        itemCount: clips.length,
        onPageChanged: (i) => setState(() => _cur = i),
        itemBuilder: (_, i) => ClipView(clip: clips[i], play: widget.active && i == _cur),
      );
}

class ClipView extends StatefulWidget {
  final Clip clip;
  final bool play;
  const ClipView({super.key, required this.clip, required this.play});
  @override
  State<ClipView> createState() => _ClipViewState();
}

class _ClipViewState extends State<ClipView> {
  late final VideoPlayerController _c;
  bool _ready = false, _liked = false;
  int _likes = 1200;

  @override
  void initState() {
    super.initState();
    _c = VideoPlayerController.asset(widget.clip.asset)
      ..setLooping(true)
      ..initialize().then((_) {
        if (!mounted) return;
        setState(() => _ready = true);
        _sync();
      });
  }

  @override
  void didUpdateWidget(ClipView old) {
    super.didUpdateWidget(old);
    _sync();
  }

  void _sync() {
    if (!_ready) return;
    widget.play ? _c.play() : _c.pause();
  }

  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  void _gifts() => showModalBottomSheet(
        context: context,
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

  Widget _rail(IconData i, String label, VoidCallback f, {Color color = Colors.white}) => Padding(
        padding: const EdgeInsets.only(bottom: 16),
        child: InkWell(
          onTap: f,
          child: Column(children: [
            Icon(i, color: color, size: 34),
            Text(label, style: const TextStyle(color: Colors.white, fontSize: 12)),
          ]),
        ),
      );

  @override
  Widget build(BuildContext context) => Container(
        color: Colors.black,
        child: Stack(fit: StackFit.expand, children: [
          if (_ready)
            GestureDetector(
              onTap: () => setState(() => _c.value.isPlaying ? _c.pause() : _c.play()),
              child: FittedBox(
                fit: BoxFit.cover,
                child: SizedBox(width: _c.value.size.width, height: _c.value.size.height, child: VideoPlayer(_c)),
              ),
            )
          else
            const Center(child: CircularProgressIndicator()),
          Positioned(
            right: 12,
            bottom: 40,
            child: Column(children: [
              _rail(_liked ? Icons.favorite : Icons.favorite_border, '$_likes', () => setState(() {
                    _liked = !_liked;
                    _likes += _liked ? 1 : -1;
                  }), color: _liked ? WL.red : Colors.white),
              _rail(Icons.comment, '84', () {}),
              _rail(Icons.card_giftcard, 'Gift', _gifts, color: WL.orange),
              _rail(Icons.share, 'Share', () {}),
            ]),
          ),
          Positioned(
            left: 14,
            bottom: 40,
            right: 90,
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisSize: MainAxisSize.min, children: [
              Text(widget.clip.user, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 16)),
              const SizedBox(height: 4),
              Text(widget.clip.caption, style: const TextStyle(color: Colors.white)),
            ]),
          ),
        ]),
      );
}
