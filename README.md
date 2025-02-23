# Chatbot
Voice Conversation Bots with LLM and VoiceVox

![screenshot_04022025_020059](https://github.com/user-attachments/assets/c5369e69-4aa7-4d9c-9c82-1d9ce3853f49)


## Requirements
- [voicevox_core.whl](https://github.com/VOICEVOX/voicevox_core/releases)
- [open_jtalk_dic_utf](https://sourceforge.net/projects/open-jtalk/files/Dictionary/)
- [onnxruntime-1.13.1](https://github.com/microsoft/onnxruntime/releases/tag/v1.13.1)

## Library
- pip install openai==0.28 SpeechRecognition pyaudio googletrans simpleaudio

## How to Run
1. tar -xvf "open_jtalk_dic_utf"
2. Edit /path/to/openjtalk_dic to open_jtalk_dic_utf
3. tar -xvf "onnxruntime-1.13.1"
4. ln -s "onnxruntime-1.13.1"/lib/libonnxruntime.so.1.13.1
5. Edit OPENAI_API_KEY to your api key
6. Run and Talk to Korean

## Future plans
1. Change from ChatGPT to Langchain
2. Optimize VoiceVox
3. ~~Change the console output language to Korean~~

## Notes
1. https://hommalab.io/posts/rpi/install-voicevox/
2. https://qiita.com/ueponx/items/186a7c859b49d996785f

## And..
Unable to verify running on Windows due to VoiceVox.
I only ran on Raspberry Pi.
