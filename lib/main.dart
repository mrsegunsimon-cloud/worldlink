import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
    systemNavigationBarColor: Colors.black,
    systemNavigationBarIconBrightness: Brightness.light,
  ));
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
      ..loadFlutterAsset('assets/web/index.html');
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        backgroundColor: const Color(0xFF050B24),
        body: SafeArea(child: WebViewWidget(controller: _c)),
      );
}
