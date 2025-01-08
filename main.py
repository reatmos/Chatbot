import openai
import speech_recognition as sr
import os
import threading
from googletrans import Translator
from pathlib import Path
from voicevox_core import VoicevoxCore, METAS
import simpleaudio as sa

# OpenAI API key setup
openai.api_key = "YOUR_OPENAI_API_KEY"

# Initialize VoicevoxCore
core = VoicevoxCore(open_jtalk_dict_dir=Path("./openjtalk"))
speaker_id = 1  # 1:ずんだもん, 2:四国めたん

def recognize_speech_from_mic(recognizer, microphone):
    """Recognize speech from the microphone and convert it to text"""
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        return recognizer.recognize_google(audio, language="ko")

def text_to_speech(text, output_file):
    """Convert text to speech using voicevox_core"""
    if not core.is_model_loaded(speaker_id):
        core.load_model(speaker_id)
    wave_bytes = core.tts(text, speaker_id)
    with open(output_file, "wb") as f:
        f.write(wave_bytes)
    # Play the generated audio
    wave_obj = sa.WaveObject.from_wave_file(output_file)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def get_chatgpt_response(prompt):
    """Get response from ChatGPT"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    translator = Translator()

    while True:
        print("Say something in Korean! (Press 'q' to quit)")
        korean_text = recognize_speech_from_mic(recognizer, microphone)
        if korean_text.lower() == 'q':
            print("Exiting...")
            break
        print(f"You said: {korean_text}")

        # Translate Korean input to Japanese
        translated_text = translator.translate(korean_text, src='ko', dest='ja').text

        # Get ChatGPT response
        chatgpt_response = get_chatgpt_response(translated_text)

        # Translate ChatGPT response to Japanese
        translated_response = translator.translate(chatgpt_response, src='en', dest='ja').text

        # Translate ChatGPT response to Korean for text output
        translated_response_ko = translator.translate(chatgpt_response, src='en', dest='ko').text
        print("Output:", translated_response_ko)

        # Convert Japanese response to speech
        text_to_speech(translated_response, "response.wav")
        os.remove("response.wav")

if __name__ == "__main__":
    main()