import argparse
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from PyPDF2 import PdfReader
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('bucket')
args = parser.parse_args()


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

        response = polly.start_speech_synthesis_task(
            OutputS3BucketName=args.bucket,
            OutputS3KeyPrefix=output_file,
            Text=text,
            VoiceId=voice_id,
            OutputFormat=output_format,
        )

        taskId = response['SynthesisTask']['TaskId']
        print(f'Task id is {taskId}')

        task_status = polly.get_speech_synthesis_task(TaskId=taskId)
        print(task_status)

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def main():
    filename = 'FAA-H-8083-16B_Chapter_1'
    pth = Path.cwd().parent.parent / 'Downloads'
    reader = PdfReader(pth / f'{filename}.pdf')
    for n, page in enumerate(reader.pages, start=1):
        if n > 6:
            text = page.extract_text()
            print(text)
            synthesize_speech(text, f'{filename}_page{n}')


if __name__ == "__main__":
    main()
