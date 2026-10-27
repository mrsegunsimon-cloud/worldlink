import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../data.dart';
import '../theme.dart';
import 'music_page.dart';

class ExplorePage extends StatefulWidget {
  const ExplorePage({super.key});
  @override
  State<ExplorePage> createState() => _ExplorePageState();
}

class _ExplorePageState extends State<ExplorePage> {
  late Future<Destinations> _f = Destinations.load();
  String _region = 'all';

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('World Tourism Centres'), actions: [
          IconButton(
            icon: const Icon(Icons.music_note),
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const MusicPage())),
          ),
        ]),
        body: FutureBuilder<Destinations>(
          future: _f,
          builder: (_, s) {
            if (!s.hasData) return const Center(child: CircularProgressIndicator());
            final d = s.data!;
            final list = _region == 'all' ? d.places : d.places.where((p) => p.region == _region).toList();
            return Column(children: [
              SizedBox(
                height: 52,
                child: ListView(scrollDirection: Axis.horizontal, padding: const EdgeInsets.symmetric(horizontal: 8), children: [
                  _chip('all', 'All'),
                  for (final r in d.regions) _chip(r.id, r.name),
                ]),
              ),
              Expanded(
                child: GridView.builder(
                  padding: const EdgeInsets.all(10),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2, mainAxisSpacing: 10, crossAxisSpacing: 10, childAspectRatio: 0.85),
                  itemCount: list.length,
                  itemBuilder: (_, i) => _tile(list[i]),
                ),
              ),
            ]);
          },
        ),
      );

  Widget _chip(String id, String name) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 8),
        child: ChoiceChip(label: Text(name), selected: _region == id, onSelected: (_) => setState(() => _region = id)),
      );

  Widget _tile(Place p) => InkWell(
        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => PlaceDetail(place: p))),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(14),
          child: Stack(fit: StackFit.expand, children: [
            Image.asset(p.photo, fit: BoxFit.cover),
            const DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Colors.transparent, Colors.black87]),
              ),
            ),
            Positioned(
              left: 10,
              bottom: 10,
              right: 10,
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(p.name, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800)),
                Text(p.country, style: const TextStyle(color: Colors.white70, fontSize: 12)),
              ]),
            ),
          ]),
        ),
      );
}

class PlaceDetail extends StatelessWidget {
  final Place place;
  const PlaceDetail({super.key, required this.place});

  Future<void> _open(String url) async {
    await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: Text(place.name)),
        body: ListView(children: [
          Image.asset(place.photo, height: 240, fit: BoxFit.cover),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('${place.name}, ${place.country}', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
              const SizedBox(height: 8),
              Text(place.blurb),
              const SizedBox(height: 16),
              FilledButton(onPressed: () => _open(place.guide), child: const Text('Open travel guide')),
              const SizedBox(height: 10),
              OutlinedButton(
                onPressed: () => _open('https://www.google.com/maps/search/?api=1&query=${Uri.encodeComponent('${place.name} ${place.country}')}'),
                child: const Text('See it in Maps'),
              ),
              const SizedBox(height: 16),
              Text('Photo: ${place.credit} (${place.license})', style: const TextStyle(fontSize: 11, color: Colors.grey)),
            ]),
          ),
        ]),
      );
}
