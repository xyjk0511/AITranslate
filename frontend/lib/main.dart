import "dart:convert";

import "package:flutter/material.dart";
import "package:http/http.dart" as http;

// Android emulator: http://10.0.2.2:8000
// Desktop / Flutter web in a browser: http://127.0.0.1:8000
// Real device on LAN: replace with your machine's LAN IP, e.g. http://192.168.x.x:8000
const String backendBaseUrl = "http://127.0.0.1:8000";

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "AI Translation Assistant",
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const TranslationPage(),
    );
  }
}

class TranslationPage extends StatefulWidget {
  const TranslationPage({super.key});

  @override
  State<TranslationPage> createState() => _TranslationPageState();
}

class _TranslationPageState extends State<TranslationPage> {
  final TextEditingController _controller = TextEditingController();
  bool _isLoading = false;
  String? _translation;
  List<String> _keywords = const [];
  String? _error;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _translate() async {
    final text = _controller.text.trim();
    if (text.isEmpty) {
      _showError("请输入要翻译的中文内容");
      return;
    }

    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final uri = Uri.parse("$backendBaseUrl/translate");
      final response = await http.post(
        uri,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"text": text}),
      );

      if (response.statusCode != 200) {
        String message = "请求失败";
        try {
          final errorJson = jsonDecode(response.body) as Map<String, dynamic>;
          message = errorJson["detail"]?.toString() ?? message;
        } catch (_) {}
        _showError(message);
        return;
      }

      final data = jsonDecode(response.body) as Map<String, dynamic>;
      final translation = data["translation"]?.toString();
      final keywordsRaw = data["keywords"];
      List<String> keywords = [];
      if (keywordsRaw is List) {
        keywords = keywordsRaw.map((e) => e.toString()).toList();
      }

      setState(() {
        _translation = translation;
        _keywords = keywords;
      });
    } catch (e) {
      _showError("网络或解析错误: $e");
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _showError(String message) {
    setState(() {
      _error = message;
    });
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(message)),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("AI 翻译助手"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _controller,
              maxLines: 5,
              minLines: 3,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: "输入中文",
                alignLabelWithHint: true,
              ),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: _isLoading ? null : _translate,
              child: const Text("翻译"),
            ),
            const SizedBox(height: 12),
            if (_isLoading) ...[
              const Center(child: CircularProgressIndicator()),
            ] else ...[
              if (_error != null)
                Text(
                  _error!,
                  style: const TextStyle(color: Colors.red),
                ),
              if (_translation != null) ...[
                const Text(
                  "英文翻译",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                Text(_translation!),
                const SizedBox(height: 8),
                const Text(
                  "关键词",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: _keywords
                      .map((k) => Text(k.isEmpty ? "(空)" : k))
                      .toList(),
                ),
              ],
            ],
          ],
        ),
      ),
    );
  }
}
