from gtts import gTTS
import os

text = "Jai Sri Krishna Ravindra Bhai, project avyan is now active."
tts = gTTS(text=text, lang='en')
tts.save("welcome.mp3")
print("[+] Audio file 'welcome.mp3' successfully generated!")
