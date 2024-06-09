import pyaudio
from six.moves import queue
import logging
from google.cloud import speech
from google.api_core.exceptions import GoogleAPICallError, RetryError
from colorama import init, Fore

# Initialize Colorama
init()

# Setup custom logger
logger = logging.getLogger('STT King')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream:
    """
    Manages the microphone stream using PyAudio. It opens the microphone,
    reads the audio in chunks, and puts these chunks into a queue to be processed.
    """
    def __init__(self, rate, chunk):
        """
        Initializes the microphone stream with specified audio rate and chunk size.
        Args:
            rate (int): The sample rate of the audio in Hz.
            chunk (int): The size of the chunks of audio data in bytes.
        """
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True
        logger.info(Fore.GREEN + "Initialized MicrophoneStream with rate {} and chunk size {}.".format(rate, chunk) + Fore.RESET)

    def __enter__(self):
        """
        Opens the audio stream and begins capturing audio.
        Returns:
            self (MicrophoneStream): The instance with the open audio stream.
        """
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        logger.info(Fore.YELLOW + "Audio stream opened and capturing started." + Fore.RESET)
        return self

    def __exit__(self, type, value, traceback):
        """
        Closes the audio stream and releases resources.
        """
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()
        logger.info(Fore.RED + "Audio stream closed and resources released." + Fore.RESET)

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """
        Callback function to handle incoming audio data and add it to the buffer.
        """
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """
        Generator that yields audio data chunks from the buffer.
        """
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

def listen_print_loop(responses):
    """
    Iterates through server responses and prints them.
    """
    for response in responses:
        if not response.results:
            continue
        result = response.results[0]
        if not result.alternatives:
            continue
        transcript = result.alternatives[0].transcript
        logger.info(Fore.CYAN + "Transcript: {}".format(transcript) + Fore.RESET)

def main():
    """
    Main function to set up the microphone stream, pass audio to Google Speech API,
    and handle responses.
    """
    logger.info(Fore.BLUE + "STT King Application Starting..." + Fore.RESET)
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='en-US',
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)
        try:
            responses = client.streaming_recognize(streaming_config, requests)
            listen_print_loop(responses)
        except GoogleAPICallError as e:
            logger.error(Fore.RED + "An error occurred during the API call: {}".format(e) + Fore.RESET)
        except RetryError as e:
            logger.error(Fore.RED + "A retry error occurred: {}".format(e) + Fore.RESET)
        except Exception as e:
            logger.error(Fore.RED + "An unexpected error occurred: {}".format(e) + Fore.RESET)
    logger.info(Fore.BLUE + "STT King Application Terminated." + Fore.RESET)

if __name__ == '__main__':
    main()
