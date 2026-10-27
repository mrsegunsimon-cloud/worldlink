import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class Place {
  final String key, name, country, region, blurb, guide, credit, license;
  const Place(this.key, this.name, this.country, this.region, this.blurb,
      this.guide, this.credit, this.license);

  String get photo => 'assets/photos/$key.jpg';

  factory Place.fromJson(Map<String, dynamic> j) => Place(
        j['key'] as String,
        j['name'] as String,
        j['country'] as String,
        j['region'] as String,
        j['blurb'] as String,
        j['guide'] as String,
        j['credit'] as String,
        j['license'] as String,
      );
}

class Region {
  final String id, name;
  const Region(this.id, this.name);
}

class Destinations {
  final List<Region> regions;
  final List<Place> places;
  const Destinations(this.regions, this.places);

  static Future<Destinations> load() async {
    final raw = await rootBundle.loadString('assets/data/destinations.json');
    final j = jsonDecode(raw) as Map<String, dynamic>;
    final regions = (j['regions'] as List)
        .map((r) => Region(r['id'] as String, r['name'] as String))
        .toList();
    final places = (j['places'] as List)
        .map((p) => Place.fromJson(p as Map<String, dynamic>))
        .toList();
    return Destinations(regions, places);
  }
}

class Song {
  final String title, artist, asset;
  const Song(this.title, this.artist, this.asset);
}

const songs = <Song>[
  Song('Lagos Nights', 'WorldLink Studio', 'assets/media/lagos_nights.mp3'),
  Song('Sunrise Highlife', 'WorldLink Studio', 'assets/media/sunrise_highlife.mp3'),
  Song('Lo-fi Study Beat', 'WorldLink Studio', 'assets/media/lofi_study.mp3'),
  Song('Savanna Drums', 'WorldLink Studio', 'assets/media/savanna_drums.mp3'),
];

class Clip {
  final String asset, title, user, caption;
  const Clip(this.asset, this.title, this.user, this.caption);
}

const clips = <Clip>[
  Clip('assets/media/lagos_nights.mp4', 'Lagos Nights', '@worldlink.studio',
      'Original demo music video #afrobeat'),
  Clip('assets/media/sunrise_highlife.mp4', 'Sunrise Highlife', '@worldlink.studio',
      'Original demo music video #highlife'),
  Clip('assets/media/savanna_drums.mp4', 'Savanna Drums', '@worldlink.studio',
      'Original demo music video #drums'),
];

const gifts = <List<Object>>[
  ['🌹', 'Rose', 1],
  ['❤️', 'Heart', 5],
  ['🎩', 'Top hat', 20],
  ['👑', 'Crown', 50],
  ['🦁', 'Lion', 200],
  ['💎', 'Diamond', 500],
  ['🚀', 'Rocket', 1000],
];
