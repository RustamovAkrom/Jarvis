import time

from recognizer.offline import OfflineRecognizer
# from recognizer.online import OnlineRecognizer

from speaker.silero_tts import Speaker
from speaker.voice_player import PlayAudio

from core.command_manager import execute_command
from core.text_analyzer import extract_commands
from core.logger import logger
from core.config import config


ASISTANT_NAMES: list[str] = config.data.get("name")
ASISTANT_LANGUAGE: str = config.data.get("language")
ASISTANT_VOSK_MODEL_PATH: str = config.data.get("recognizer").get("model_path")
ASISTANT_AFTER_KEY_WORD_TIMEOUT: int = config.data.get("voice_timeout")


def main():
    play_audio.play("run")

    last_time = time.time() - 1000

    while True:
        voice_text = offline_recognition.listen().lower()

        if voice_text and is_activation_command(voice_text):
            play_audio.play("great")
            
            execute_cmd(voice_text)

            time.sleep(0.5)

            last_time = time.time()

            while (time.time() - last_time) <= 15:
                voice_text = offline_recognition.listen()
                print(f"Recognized text: {voice_text}")

                execute_cmd(voice_text)


def is_activation_command(text: str):
    for activation_word in ASISTANT_NAMES:
        if activation_word in text:
            return True
        return False
    

def execute_cmd(text: str):
    commands = extract_commands(text)

    if commands:
        play_audio.play("ok")

        for command, args in commands:
            print(f"Command: {command}, Args: {args}.")

            result = execute_command(command, args)
            print(f"Result: {result}.")
            if result:
                speaker.say(result)


if __name__=='__main__':
    print("Initializing...")
    logger.info("Initializing...")

    offline_recognition = OfflineRecognizer(ASISTANT_VOSK_MODEL_PATH)
    play_audio = PlayAudio()
    speaker = Speaker()

    main()
