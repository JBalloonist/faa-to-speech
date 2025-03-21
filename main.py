import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from PyPDF2 import PdfReader
from pathlib import Path


def synthesize_speech(text, output_file="output.mp3", voice_id="Joanna", output_format="mp3"):
    """
    Synthesizes speech from the given text using Amazon Polly and saves it to an MP3 file.

    Args:
        text (str): The text to synthesize.
        output_file (str): The name of the output MP3 file.
        voice_id (str): The ID of the voice to use (e.g., "Joanna", "Matthew").
        output_format (str): The desired output format (e.g., "mp3", "pcm", "ogg_vorbis").

    Returns:
        bool: True if the synthesis was successful, False otherwise.
    """
    try:
        polly = boto3.client("polly")

        response = polly.synthesize_speech(
            Text=text,
            VoiceId=voice_id,
            OutputFormat=output_format,
        )

        if "AudioStream" in response:
            with open(output_file, "wb") as f:
                f.write(response["AudioStream"].read())
            print(f"Speech synthesized and saved to {output_file}")
            return True
        else:
            print("Could not synthesize speech")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def main():
    filename = 'FAA-H-8083-16B_Chapter_1'
    pth = Path.cwd().parent.parent / 'Downloads'
    reader = PdfReader(pth / f'{filename}.pdf')
    for n, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        print(text)

        if synthesize_speech(text, f'{filename}_page{n}'):
            print("Success")
        else:
            print("Failure")
        if n > 6:
            break


if __name__ == "__main__":
    main()
