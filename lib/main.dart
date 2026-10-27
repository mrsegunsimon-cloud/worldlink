import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:webview_flutter/webview_flutter.dart';

bool fbReady = false;

Future<void> initFirebase() async {
  try {
    final j = jsonDecode(await rootBundle.loadString('assets/firebase_config.json')) as Map<String, dynamic>;
    final key = (j['apiKey'] ?? '') as String;
    if (key.isEmpty) return;
    await Firebase.initializeApp(
      options: FirebaseOptions(
        apiKey: key,
        appId: j['appId'] as String,
        projectId: j['projectId'] as String,
        messagingSenderId: (j['messagingSenderId'] ?? '') as String,
        storageBucket: (j['storageBucket'] ?? '') as String,
      ),
    );
    fbReady = true;
  } catch (e) {
    debugPrint('Firebase init failed: $e');
  }
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
    systemNavigationBarColor: Colors.black,
    systemNavigationBarIconBrightness: Brightness.light,
  ));
  await initFirebase();
  runApp(const WorldLinkApp());
}

class WorldLinkApp extends StatelessWidget {
  const WorldLinkApp({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'WorldLink',
        debugShowCheckedModeBanner: false,
        theme: ThemeData.dark(useMaterial3: true),
        home: const WorldLinkShell(),
      );
}

class WorldLinkShell extends StatefulWidget {
  const WorldLinkShell({super.key});
  @override
  State<WorldLinkShell> createState() => _WorldLinkShellState();
}

class _WorldLinkShellState extends State<WorldLinkShell> {
  late final WebViewController _c;

  @override
  void initState() {
    super.initState();
    _c = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0xFF050B24))
      ..addJavaScriptChannel('WLAuth', onMessageReceived: _onMsg)
      ..loadFlutterAsset('assets/web/index.html');
  }

  Map<String, dynamic> _user(User? u) =>
      u == null ? {'user': null} : {'user': {'uid': u.uid, 'email': u.email ?? ''}};

  String _human(FirebaseAuthException e) {
    switch (e.code) {
      case 'email-already-in-use':
        return 'That email already has an account. Tap "I already have an account".';
      case 'invalid-email':
        return 'That email address is not valid.';
      case 'weak-password':
        return 'Password is too weak. Use 8 or more characters.';
      case 'wrong-password':
      case 'invalid-credential':
      case 'user-not-found':
        return 'Wrong email or password.';
      case 'network-request-failed':
        return 'No internet connection. Try again.';
      case 'too-many-requests':
        return 'Too many tries. Wait a minute and try again.';
      case 'operation-not-allowed':
        return 'Email login is not switched on in Firebase yet.';
      default:
        return 'Could not complete that (${e.code}).';
    }
  }

  Future<Map<String, dynamic>> _handle(Map<String, dynamic> j) async {
    final op = j['op'] as String;
    if (!fbReady) {
      return op == 'state' ? {'user': null} : {'error': 'Online accounts are not switched on in this build yet.'};
    }
    final a = FirebaseAuth.instance;
    switch (op) {
      case 'state':
        return _user(a.currentUser);
      case 'signup':
        final cr = await a.createUserWithEmailAndPassword(email: j['email'] as String, password: j['password'] as String);
        try {
          await cr.user?.sendEmailVerification();
        } catch (_) {}
        return _user(cr.user);
      case 'login':
        final cr = await a.signInWithEmailAndPassword(email: j['email'] as String, password: j['password'] as String);
        return _user(cr.user);
      case 'reset':
        await a.sendPasswordResetEmail(email: j['email'] as String);
        return {'ok': true};
      case 'logout':
        await a.signOut();
        return {'ok': true};
    }
    return {'error': 'Unknown request.'};
  }

  Future<void> _onMsg(JavaScriptMessage m) async {
    final j = jsonDecode(m.message) as Map<String, dynamic>;
    Map<String, dynamic> r;
    try {
      r = await _handle(j);
    } on FirebaseAuthException catch (e) {
      r = {'error': _human(e)};
    } catch (e) {
      r = {'error': 'Something went wrong. Try again.'};
    }
    await _c.runJavaScript('window.__wlReply(${j['id']}, ${jsonEncode(r)})');
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        backgroundColor: const Color(0xFF050B24),
        body: SafeArea(child: WebViewWidget(controller: _c)),
      );
}
