# from deepgram import DeepgramClient
# from dotenv import load_dotenv
# from pathlib import Path
# import os

# from dotenv import load_dotenv

# load_dotenv()

# api_key = os.getenv("DEEPGRAM_API_KEY", "").strip()



# if not api_key:
#     raise ValueError("DEEPGRAM_API_KEY not found in .env")

# text="Hello,i am sujan , nice to meet you. What can i do for you?Hope you are very well."

# deepgram = DeepgramClient(api_key=api_key)
# audio = deepgram.speak.v1.audio.generate(
#         text=text,
#         model=os.environ.get("DEEPGRAM_TTS_MODEL", "aura-2-thalia-en"),
#         encoding="mp3",
#     )






# # Step 3: Save audio
# audio_file="test-output.mp3"
# audio_path = Path(__file__).resolve().with_name(audio_file)

# with audio_path.open("wb") as file:
#     for chunk in audio:
#         file.write(chunk)






# # Step 4: Play Audio
# # Step4: Play audio
# import platform
# import subprocess


# if platform.system() == "Darwin":  # macOS
#     subprocess.run(["afplay", str(audio_path)])
# elif platform.system() == "Windows":
#     os.startfile(audio_path)
# else:  # Linux
#     subprocess.run(["xdg-open", str(audio_path)])







# Step1: Create API keys

# Step2: Create Client and send request
from deepgram import DeepgramClient
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DOCTOR_AUDIO = BASE_DIR / "doctor_response.mp3"
def convert_text_to_doctor_audio(text, output_filepath=DEFAULT_DOCTOR_AUDIO):
    deepgram_api_key = os.environ.get("DEEPGRAM_API_KEY")
    deepgram = DeepgramClient(api_key=deepgram_api_key)
    audio = deepgram.speak.v1.audio.generate(
        text=text,
        model=os.environ.get("DEEPGRAM_TTS_MODEL", "aura-2-thalia-en"),
        encoding="mp3",
    )

    output_filepath = Path(output_filepath)
    with output_filepath.open("wb") as file:
        for chunk in audio:
            file.write(chunk)

    return output_filepath

import subprocess
import platform
def play_audio(audio_filepath):
    audio_filepath = str(audio_filepath)

    if platform.system() == "Darwin":
        subprocess.run(["afplay", audio_filepath], check=False)
    elif platform.system() == "Windows":
        os.startfile(audio_filepath)
    else:
        subprocess.run(["xdg-open", audio_filepath], check=False)