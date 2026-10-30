
# # Step 1: Install and import dependencies
# from openai import OpenAI
# from dotenv import load_dotenv
# import os
# # Step 2: Create api key and  Client

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=api_key)

# # Step 3: Create message
# messages=[
#   {
#     "role":"user",
#     "content":[
#       {
#       "type":"text",
#       "text":"Hello, what can you help me with?"
#       }
#     ]
#   }
# ]


# # Step 4: Send Message

# response = client.chat.completions.create(
#     model="gpt-4.1-mini",
#     max_tokens=1000,
#     messages=messages
# )

# # Step 5: Print Response
# print(response.choices[0].message.content)







# # Step 1: Install and import dependencies
# from anthropic import Anthropic
# from dotenv import load_dotenv
# import os
# import base64

# # Step 2: Load API key and create client
# load_dotenv()

# api_key = os.getenv("MINIMAX_API_KEY")
# client = Anthropic(
#     api_key=api_key,
#     base_url="https://api.minimax.io/anthropic"
# )

# # Step 3: Get image path
# folder = os.path.dirname(__file__)
# image_path = os.path.join(folder, "sample_image.jpg")

# # Step 4: Read and encode image
# with open(image_path, "rb") as file:
#     image_data = base64.b64encode(file.read()).decode("utf-8")

# # Step 5: Create image message
# image_messages = [
#     {
#         "role": "user",
#         "content": [
#             {
#                 "type": "text",
#                 "text": "What do you see in this image?"
#             },
#             {
#                 "type": "image",
#                 "source": {
#                     "type": "base64",
#                     "media_type": "image/jpeg",
#                     "data": image_data
#                 }
#             }
#         ]
#     }
# ]
# # Video Messages

# video_path = os.path.join(folder, "test-video.mp4")
# with open(video_path, "rb") as file:
#     video_data = base64.b64encode(file.read()).decode("utf-8")

# video_messages = [
#     {
#         "role": "user",
#         "content": [
#             {
#                 "type": "video",
#                 "source": {
#                     "type": "base64",
#                     "media_type": "video/mp4",
#                     "data": video_data,
#                 },
#             },
#             {
#                 "type": "text",
#                 "text": "What is happening in this video?",
#             },
#         ],
#     }
# ]
# # Step 6: Send message
# response = client.messages.create(
#     model="MiniMax-M3",
#     max_tokens=1000,
#    messages=video_messages
# )


# for block in response.content:
#     if block.type == "text":
#         print(block.text)










# Step1: Install and import dependencies
import anthropic
from dotenv import load_dotenv
import os
import base64
import mimetypes
# Step2: Create API keys & Client

load_dotenv()


def encode_file(filepath):
    with open(filepath, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def get_media_type(filepath, fallback):
    media_type, _ = mimetypes.guess_type(filepath)
    return media_type or fallback


def brain_of_the_doctor(patient_text, image_filepath=None, video_filepath=None):

    minimax_api_key = os.environ.get("MINIMAX_API_KEY")

    prompt = (
    "You are a confident, natural doctor specializing in skin care. Speak with the reassurance, clarity, and authority of a real doctor. "
    "Limit your entire response to two or three sentences maximum. "
    "If the patient has not provided a video and only an image, your absolute priority is to ask them to provide a video first because mention that you need more details and you need a video showing the problem. "
    "Do not use any special characters, symbols, asterisks, or markdown formatting in your response because it will be converted directly to audio.\n\n"
    f"Patient text: {patient_text}"
)

    if video_filepath:
        media_content = {
            "type": "video",
            "source": {
                "type": "base64",
                "media_type": get_media_type(video_filepath, "video/mp4"),
                "data": encode_file(video_filepath),
            },
        }
    else:
        media_content = {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": get_media_type(image_filepath, "image/png"),
                "data": encode_file(image_filepath),
            },
        }

    client = anthropic.Anthropic(
        api_key=minimax_api_key,
        base_url=os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.io/anthropic"),
    )
    response = client.messages.create(
        model=os.environ.get("MINIMAX_MODEL", "MiniMax-M3"),
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [media_content, {"type": "text", "text": prompt}],
            }
        ],
    )

    doctors_response_in_text = response.content[0].text

    return doctors_response_in_text
