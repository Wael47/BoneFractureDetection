import 'package:path/path.dart';
import 'package:async/async.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Bone Fracture Detection',
      home: MyStatefulWidget(),
    );
  }
}

class MyStatefulWidget extends StatefulWidget {
  const MyStatefulWidget({super.key});

  @override
  _MyStatefulWidgetState createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget> {
  File? _image;
  var _imagePrediction;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bone Fracture Detection'),
        centerTitle: true,
        backgroundColor: Colors.cyan,
      ),
      body: Center(
        child: Container(
          decoration: const BoxDecoration(
            image: DecorationImage(
              image: AssetImage("assets/AI-health.png"),
              fit: BoxFit.cover,
            ),
          ),
          padding:
              const EdgeInsets.only(top: 20, bottom: 20, left: 20, right: 20),
          alignment: Alignment.center,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _image == null ? Container() : Image.file(_image as File),
              const SizedBox(
                height: 20,
              ),
              Center(
                child: Visibility(
                  visible: _imagePrediction != null,
                  child: Padding(padding: const EdgeInsets.all(15),
                    child: Text(
                      "$_imagePrediction",
                      textAlign: TextAlign.center,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 24,
                        color: Colors.blue,
                        backgroundColor: Colors.white,
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: BottomAppBar(
        shape: const CircularNotchedRectangle(),
        child: Container(height: 20.0),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => pickImage(),
        tooltip: 'Select X-RAY Image',
        child: const Icon(Icons.image),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
    );
  }

  pickImage() async {
    final image = await ImagePicker().pickImage(
      source: ImageSource.gallery,
      maxWidth: 500,
      maxHeight: 500,
    );
    if (image != null) {
      _image = File(image.path);
      upload(_image!);
      _imagePrediction = '';
      setState(() {});
    }
  }

  upload(File imageFile) async {
    final url = Uri.parse('http://172.19.1.50:8000/api');

    // Create a multipart request
    final request = http.MultipartRequest('POST', url);

    // Add the image file to the request
    request.files
        .add(await http.MultipartFile.fromPath('image', imageFile.path));

    // Send the request and get the response
    final response = await request.send();

    if (response.statusCode == 201) {
      final responseData = await response.stream.transform(utf8.decoder).join();
      Map<String, dynamic> responseMap = json.decode(responseData);
      int prediction = responseMap['prediction'];
      print(prediction);
      _imagePrediction = prediction == 1 ? 'Fractured' : 'Normal';
      setState(() {});
    } else {
      print('Image sending failed with status code: ${response.statusCode}');
    }
  }
}
