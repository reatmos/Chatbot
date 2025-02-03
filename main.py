import openai
import speech_recognition as sr
import os
import asyncio
from googletrans import Translator
from pathlib import Path
from voicevox_core import VoicevoxCore, METAS
import simpleaudio as sa

# OpenAI API key setup
openai.api_key = "OPENAI_API_KEY"

# Initialize VoicevoxCore
core = VoicevoxCore(open_jtalk_dict_dir=Path("/path/to/openjtalk_dic"))
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
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

async def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    translator = Translator()
    
    while True:
        korean_text = recognize_speech_from_mic(recognizer, microphone)
        
        print(f"\nYou said: {korean_text}")
        
        # Translate Korean input to English
        translated_text = await translator.translate(korean_text, src='ko', dest='en')
        
        # Get AI response
        chatgpt_response = get_chatgpt_response(translated_text.text)
        
        # Translate AI response to Korean for text output
        translated_response_ko = await translator.translate(chatgpt_response, src='en', dest='ko')
        print("Output:", translated_response_ko.text)

        # Translate AI response to Japanese for speech output
        translated_response = await translator.translate(chatgpt_response, src='en', dest='ja')
        text_to_speech(translated_response.text, "response.wav")
        os.remove("response.wav")

if __name__ == "__main__":
    asyncio.run(main())
