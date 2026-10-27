import 'package:flutter/material.dart';
import 'package:just_audio/just_audio.dart';
import '../data.dart';
import '../theme.dart';

class MusicPage extends StatefulWidget {
  const MusicPage({super.key});
  @override
  State<MusicPage> createState() => _MusicPageState();
}

class _MusicPageState extends State<MusicPage> {
  final _p = AudioPlayer();
  int? _i;

  @override
  void dispose() {
    _p.dispose();
    super.dispose();
  }

  Future<void> _play(int i) async {
    if (_i == i) {
      _p.playing ? await _p.pause() : await _p.play();
      setState(() {});
      return;
    }
    setState(() => _i = i);
    try {
      await _p.setAsset(songs[i].asset);
      await _p.play();
    } catch (e) {
      debugPrint('audio error $e');
    }
    if (mounted) setState(() {});
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('Music')),
        body: ListView.builder(
          itemCount: songs.length,
          itemBuilder: (_, i) => ListTile(
            leading: CircleAvatar(
              backgroundColor: WL.blue,
              child: Icon(_i == i && _p.playing ? Icons.pause : Icons.play_arrow, color: Colors.white),
            ),
            title: Text(songs[i].title),
            subtitle: Text(songs[i].artist),
            onTap: () => _play(i),
          ),
        ),
        bottomNavigationBar: _i == null
            ? null
            : StreamBuilder<Duration>(
                stream: _p.positionStream,
                builder: (_, s) {
                  final d = _p.duration?.inMilliseconds ?? 1;
                  final v = (s.data?.inMilliseconds ?? 0) / (d == 0 ? 1 : d);
                  return SafeArea(
                    child: Column(mainAxisSize: MainAxisSize.min, children: [
                      LinearProgressIndicator(value: v.clamp(0.0, 1.0)),
                      ListTile(
                        title: Text(songs[_i!].title),
                        subtitle: Text(songs[_i!].artist),
                        trailing: IconButton(
                          icon: Icon(_p.playing ? Icons.pause : Icons.play_arrow),
                          onPressed: () => _play(_i!),
                        ),
                      ),
                    ]),
                  );
                },
              ),
      );
}
