"""
Wav/ogg conversion -> text.
"""

import json
import os
import subprocess

from vosk import KaldiRecognizer, Model  # Offline recognition from Vosk.


class STT:
    """
    Class for recognizing audio via Vosk and converting it to text.
    Audio formats supported: wav, ogg.
    """
    default_init = {
        "model_path": "models/vosk/model",  # Path to the folder with the Vosk model STT files.
        "sample_rate": 16000,
        "ffmpeg_path": "models/vosk"  # Path to ffmpeg.
    }

    def __init__(
            self,
            model_path=None,
            sample_rate=None,
            ffmpeg_path=None
    ) -> None:
        """
        Configuring the Vosk model to recognize audio and
        convert it to text.
        :arg model_path: str path to the Vosk model.
        :arg sample_rate: int sampling rate, usually 16000.
        :arg ffmpeg_path: str path to ffmpeg.
        """

        self.model_path = model_path if model_path else STT.default_init["model_path"]
        self.sample_rate = sample_rate if sample_rate else STT.default_init["sample_rate"]
        self.ffmpeg_path = ffmpeg_path if ffmpeg_path else STT.default_init["ffmpeg_path"]

        self._check_model()

        model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(model, self.sample_rate)
        self.recognizer.SetWords(True)

    def _check_model(self):
        """
        Checking the availability of the Vosk model in the desired language in the application catalog.
        """
        print(self.model_path)
        if not os.path.exists(self.model_path):
            raise Exception(
                "Vosk: save the model folder to the vosk folder\n"
                "Download the model from the link https://alphacephei.com/vosk/models"
            )

        isffmpeg_here = False
        for file in os.listdir(self.ffmpeg_path):
            if file.startswith('ffmpeg'):
                isffmpeg_here = True

        if not isffmpeg_here:
            raise Exception(
                "Ffmpeg: Save ffmpeg.exe to the ffmpeg folder\n"
                "Download ffmpeg.exe by the link https://ffmpeg.org/download.html"
            )
        self.ffmpeg_path = self.ffmpeg_path + '/ffmpeg'

    async def audio_to_text(self, audio_file_name=None) -> str:
        """
        Offline-recognition of audio to text via Vosk.
        :param audio_file_name: str path and name of the audio file.
        :return: str recognized text.
        """

        if audio_file_name is None:
            raise Exception("Specify the path and file name")
        if not os.path.exists(audio_file_name):
            raise Exception("Specify the correct path and file name")

        # Convert audio to wav and the result to process.stdout.
        process = subprocess.Popen(
            [self.ffmpeg_path,
             "-loglevel", "quiet",
             "-i", audio_file_name,  # input file name.
             "-ar", str(self.sample_rate),  # sampling rate.
             "-ac", "1",  # number of channels.
             "-f", "s16le",  # codec for transcoding, we have wav.
             "-"  # there is no output file name, we read it from stdout.
             ],
            stdout=subprocess.PIPE
        )

        # Reading data in chunks and recognizing through the model.
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                pass

        # We return the recognized text in the form of str.
        result_json = self.recognizer.FinalResult()  # this is json in the form of str.
        result_dict = json.loads(result_json)  # this is dict.
        return result_dict["text"]  # text in the form of str.
