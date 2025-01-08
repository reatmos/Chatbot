# Chatbot
Voice Conversation Bots with LLM and VoiceVox

![Wed  8 Jan 18:32:51 KST 2025](https://github.com/user-attachments/assets/099dd60d-b8ed-4413-8af7-d0ad60727e45)


## Requirements
- [Open_JTalk](https://open-jtalk.sourceforge.net/)
- [OnnxRuntime 1.13.1](https://github.com/microsoft/onnxruntime/releases/tag/v1.13.1)

## Library
- openai
- SpeechRecognition
- googletrans==4.0.0-rc1
- [voicevox-core](https://github.com/VOICEVOX/voicevox_core) - Install whl over pip
- simpleaudio

## How to Run
1. tar -xvf "Open_JTalk"
2. Edit open_jtalk_dict_dir Path
3. ln -s "OnnxRuntime"/lib/libonnxruntime.so.1.13.1
4. Edit openai.api_key
5. Run and Talk Korean
6. Exit is input to 'q'
