from google.cloud import speech
import os

def stream_file(file_path: str):
    """
    Streams the transcription of the given audio file using Google Cloud Speech API.
    
    Args:
    file_path (str): The path to the audio file to transcribe.
    """
    client = speech.SpeechClient()
    
    # Prepare the audio file for streaming by chunking the data
    def stream_audio_file():
        with open(file_path, 'rb') as audio_file:
            while True:
                data = audio_file.read(4096)  # Read in chunks of 4KB
                if not data:
                    break
                yield data
    
    # Configure the recognition request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US'
    )
    
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True  # Set to True if you want interim results, otherwise set to False
    )
    
    # Construct the streaming request from the audio data generator
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream_audio_file())
    
    # A generator that yields responses
    responses = client.streaming_recognize(config=streaming_config, requests=requests)
    
    # Process responses
    for response in responses:
        for result in response.results:
            print('Finished:', result.is_final)
            print('Stability:', result.stability)
            alternatives = result.alternatives
            for alternative in alternatives:
                print('Confidence:', alternative.confidence)
                print('Transcript:', alternative.transcript)

# Example usage
if __name__ == "__main__":
    # Path to your audio file, adjust sample_rate_hertz and encoding according to your file's specs
    audio_file_path = "/path/to/your/audiofile.wav"
    stream_file(audio_file_path)
