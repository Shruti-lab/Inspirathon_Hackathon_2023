import numpy as np
import cv2
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))
from pytube import YouTube
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"D:\Websites\VideoGlancer\Notesmaker\notesmaker\Tesseract-OCR\tesseract.exe"
import speech_recognition as sr
import moviepy.editor

def vidgentext(link):
    Download(link)
    ocr()
    return s2t(r"D:\Websites\VideoGlancer\Notesmaker\notesmaker\video.mp4")

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download(output_path="D:\\Websites\\VideoGlancer\\Notesmaker\\notesmaker\\",filename="video.mp4")
    except:
        print("An error has occurred")
    print("Download is completed successfully")

# Function to filter out meaningful words
def filter_meaningful_words(text):
    # Tokenize the text into words
    words = word_tokenize(text.lower())
    
    # Remove stopwords and words with less than 3 characters
    meaningful_words = [word for word in words if word not in stop_words and len(word) >= 3]
    
    # You can add more criteria to determine meaningfulness here
    
    return meaningful_words


def ocr():
    maxlen = 0
    cap = cv2.VideoCapture(r"D:\Websites\VideoGlancer\Notesmaker\notesmaker\video.mp4")
    if not cap.isOpened():
      print("Cannot open camera")
      exit()
    i = 0
    while i<4:
    # Capture frame-by-frame
      ret, frame = cap.read()

    # if frame is read correctly ret is True
      if not ret:
          print("Can't receive frame (stream end?). Exiting ...")
          break
    # Our operations on the frame come here
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      custom_config = r'--oem 3 --psm 6'
      random_string = pytesseract.image_to_string(gray, config=custom_config)
      if len(random_string.split()) > maxlen:
          maxlen = len(random_string.split())
          cv2.imwrite('board'+str(i)+'.png',frame)
          i+=1
      #topics_list = filter_meaningful_words(random_string)
    cap.release()
    #return topics_list



def s2t(video_path):
    video = moviepy.editor.VideoFileClip(video_path)

    #Extract the Audio
    audio = video.audio

    #Export the Audio
    audio.write_audiofile(r"D:\Websites\VideoGlancer\Notesmaker\notesmaker\Audio.wav")
    #Initiаlize  reсоgnizer  сlаss  (fоr  reсоgnizing  the  sрeeсh)
    r = sr.Recognizer()
    text = ""
    # Reading Audio file as source
    #  listening  the  аudiо  file  аnd  stоre  in  аudiо_text  vаriаble
    with sr.AudioFile(r"D:\Websites\VideoGlancer\Notesmaker\notesmaker\Audio.wav") as source:
        while True:
            audio_text = r.listen(source,timeout=None)
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
            try:
            # using google speech recognition
                # text += r.recognize_google(audio_text,language='hi-IN')
                text += r.recognize_google(audio_text)
            except:
                print("Text from s2t:",text)
                return text
            

if __name__=="__main__":
    link = "https://www.youtube.com/shorts/OZ4bsbf0Pdc"
    Download(link)
    print(s2t(r"D:\Websites\VideoGlancer\Notesmaker\notesmaker\video.mp4"))