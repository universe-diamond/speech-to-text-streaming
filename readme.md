
```markdown
# Real-Time Audio Transcription Using Google Speech-to-Text API

This project demonstrates how to implement real-time audio transcription using the Google Speech-to-Text API. The application captures audio from the microphone, streams it to the Google Speech API, and prints the transcription live.

## Prerequisites

Before you can run this project, you need the following:
- A Google Cloud account.
- A Google Cloud project with the Speech-to-Text API enabled.
- Billing enabled on your Google Cloud account.
- Python 3 installed on your machine.

## Setup

### 1. Google Cloud Setup

- Follow Google's official guide to [set up a Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) and enable the Speech-to-Text API.
- Create and download a service account key from the Google Cloud Console. This key will authenticate your API requests.

### 2. Local Environment Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install Dependencies**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

   **For macOS Users:**
   If you encounter issues installing PyAudio (e.g., missing `portaudio.h`), you need to install PortAudio first. Run:
   ```bash
   brew install portaudio
   ```
   Then, try installing PyAudio again:
   ```bash
   pip install pyaudio
   ```

3. **Set Environment Variable**
   Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the JSON file that contains your service account key.
   - On Linux/Mac:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS= "../../configs/creds.json"
     ```
   - On Windows:
     ```cmd
     set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\service-account-file.json
     ```

## Running the Application

To run the application, execute the following command in the terminal:

```bash
python src/script.py
```

Speak into your microphone. The script should print what you say as it receives the transcription results from Google's Speech-to-Text API.

## Troubleshooting

- **Audio Device Issues**: If you encounter issues with PyAudio not recognizing your microphone, ensure your audio devices are correctly configured and accessible by PyAudio.
- **API Errors**: If you see errors related to the Google Speech-to-Text API, ensure your API is enabled and your billing information is correct on the Google Cloud Console.
- **Microphone Permissions**: Make sure Python and your terminal have the necessary permissions to access your microphone. This might require adjusting system or security settings on your operating system.
- **Audio Quality**: Ensure you are using a good quality microphone and that it is correctly configured in your system settings to optimize transcription accuracy.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the functionality or documentation of this project.

## License

The project is licensed under the MIT License.
```
# Speech-to-Text-Streaming
