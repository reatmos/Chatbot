import speech_recognition as sr
from ollama import Client
from typing import Generator
from translate import Translator  # translate.Translator 사용
from pathlib import Path
from voicevox_core import VoicevoxCore
import simpleaudio as sa
import os
import asyncio

# Initialize VoicevoxCore
core = VoicevoxCore(open_jtalk_dict_dir=Path("/path/to/openjtalk"))
speaker_id = 1  # 1:ずんだもん, 2:四国めたん

class OllamaClientChatBot:
    def __init__(
        self,
        model: str = "exaone3.5:2.4b-instruct-q4_K_M",
        system_prompt: str = "당신은 친절한 어시스턴스입니다. 대답은 간결하게 해주세요.",
        max_history: int = 5
    ):
        self.client = Client(host="http://localhost:11434")
        self.model = model
        self.system_prompt = system_prompt
        self.max_history = max_history
        self.messages = [
            {"role": "system", "content": system_prompt}
        ]

    def _trim_history(self):
        """최근 대화 기록만 유지"""
        if len(self.messages) > self.max_history * 2 + 1:
            self.messages = [self.messages[0]] + self.messages[-(self.max_history * 2):]

    def stream_chat(self, user_input: str) -> Generator[str, None, None]:
        """스트리밍 채팅 응답 생성"""
        self.messages.append({"role": "user", "content": user_input})
        
        full_response = []
        stream = self.client.chat(
            model=self.model,
            messages=self.messages,
            stream=True
        )
        
        try:
            for chunk in stream:
                if chunk['message']['content']:
                    chunk_content = chunk['message']['content']
                    full_response.append(chunk_content)
                    yield chunk_content
                    
            self.messages.append({"role": "assistant", "content": "".join(full_response)})
            self._trim_history()
            
        except Exception as e:
            yield f"\n[ERROR: {str(e)}]"

def recognize_speech_from_mic(recognizer, microphone):
    """마이크로부터 음성을 인식하고 텍스트로 변환"""
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("듣고 있습니다... (음성 입력을 기다리는 중)")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio, language="ko-KR")
        except sr.UnknownValueError:
            print("음성을 이해할 수 없습니다.")
            return None
        except sr.RequestError as e:
            print(f"Google Speech Recognition 서비스에 접근할 수 없습니다: {e}")
            return None

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

async def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    translator = Translator(to_lang="ja", from_lang="ko")  # translate.Translator 사용
    
    # 챗봇 초기화
    bot = OllamaClientChatBot(
        model="exaone3.5:2.4b-instruct-q4_K_M",
        system_prompt="대답은 한국어로 간결하게 해주세요.",
        max_history=3
    )

    print("챗봇을 시작합니다 (종료: '종료'라고 말하세요)")
    while True:
        try:
            # 음성 입력 받기
            user_input = recognize_speech_from_mic(recognizer, microphone)
            if user_input is None:
                continue

            print(f"\nYou: {user_input}")
            if user_input.lower() in ["종료", "끝"]:
                print("대화를 종료합니다.")
                break

            # 챗� 응답 스트리밍 출력 및 전체 응답 수집
            print("Bot:", end=" ", flush=True)
            response_chunks = []
            for chunk in bot.stream_chat(user_input):
                print(chunk, end="", flush=True)
                response_chunks.append(chunk)
            print()

            full_response = "".join(response_chunks)
            # 텍스트를 일본어로 번역 후 출력
            translated_text = translator.translate(full_response)
            print("翻訳 (Japanese):", translated_text)
            
            # Voicevox를 사용하여 일본어로 음성 출력
            text_to_speech(translated_text, "response.wav")
            os.remove("response.wav")

        except KeyboardInterrupt:
            print("\n대화를 종료합니다.")
            break

if __name__ == "__main__":
    asyncio.run(main())
