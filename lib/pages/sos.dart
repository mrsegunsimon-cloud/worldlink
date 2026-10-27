import 'package:flutter/material.dart';
import '../theme.dart';

class SosButton extends StatelessWidget {
  const SosButton({super.key});
  @override
  Widget build(BuildContext context) => Material(
        color: WL.red,
        shape: const StadiumBorder(),
        child: InkWell(
          customBorder: const StadiumBorder(),
          onTap: () => showModalBottomSheet(
            context: context,
            builder: (_) => const Padding(
              padding: EdgeInsets.all(20),
              child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Emergency help', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800)),
                SizedBox(height: 8),
                Text('Call your local emergency number now. Sharing your live location with trusted contacts will be added in the next build.'),
              ]),
            ),
          ),
          child: const Padding(
            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            child: Text('SOS', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900)),
          ),
        ),
      );
}
