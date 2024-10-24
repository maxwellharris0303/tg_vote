from pydub import AudioSegment # pip install SpeechRecognition pydub
import whisper

# Replace 'path/to/your/audio_file.mp3' with the path to your MP3 file
mp3_audio = AudioSegment.from_mp3('audio (1).mp3')

# Convert MP3 to WAV
wav_path = 'audio_file.wav'
mp3_audio.export(wav_path, format='wav')

model = whisper.load_model("base")
result = model.transcribe(wav_path, fp16=False)

print(result['text'])