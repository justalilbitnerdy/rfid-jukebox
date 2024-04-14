import time
from pygame import mixer
import sys
from mutagen.mp3 import MP3
from lib.drive import Drive
from lib.drive import SongNotFound
import argparse
import signal
from lib.rfid import RFIDReader
import threading

mountpoint = "usb/"
currentProgress = 0
SEC_TO_MS = 1000

inputMode = "interactive"
outputMode = "tty"
rfidReader = None
stop = False
currentSong = None

def playSongThread(filePath):
  thread = threading.Thread(target=playSong, args=(filePath,))
  thread.start()
  return thread

def playSong(filePath):
  global currentSong
  if filePath != currentSong:
    currentSong = filePath
    mixer.music.stop()
    trackLength = MP3(filePath).info.length*SEC_TO_MS
    mixer.music.load(filePath)
    mixer.music.play()
    while mixer.music.get_busy():
      # if mixer.music.get_pos()>10000:
      #   mixer.music.stop()
      #   break
      printProgress(mixer.music.get_pos(),trackLength)
    currentSong = None
    print()

def printProgress(currentPos,trackLength):
  global outputMode
  if outputMode == "tty":
    printProgressTTY(currentPos,trackLength)
  if outputMode == "lcd":
    printProgressLCD(currentPos,trackLength)
  if outputMode == "none":
    pass

def printProgressTTY(currentPos,trackLength):
  global currentProgress
  if int(currentPos/trackLength*100) != currentProgress:
    currentProgress = int(currentPos/trackLength*100)
    remaining = 100 - currentProgress
    stars = "|" + "*" * currentProgress + " " * remaining + "|"
    sys.stdout.write('\r{}'.format(stars))
    sys.stdout.flush()

def printProgressLCD(currentPos,trackLength):
  global rfidReader
  if rfidReader == None:
    rfidReader
    reader = RFIDReader()
  pass

def playNextSong(drive):
  global inputMode
  print(inputMode)
  if inputMode == "interactive":
    return getNextSongInteractive()
  if inputMode == "rfid":
    return getNextSongRFID()

def getNextSongRFID():
  global rfidReader
  if rfidReader == None:
    rfidReader = RFIDReader()
  id = rfidReader.getNextID()
  print(id)
  songPath = drive.getSong(id)
  if songPath !=None:
    playSongThread(songPath)
  
  return True

def getNextSongInteractive():
  userInput = input("enter NFC ID: ")
  songPath = drive.getSong(userInput)
  if songPath !=None:
    playSongThread(songPath)
  return True

def stopListening(signal,frame):
  global stop
  mixer.music.stop()
  exit()

if __name__ == "__main__":
  signal.signal(signal.SIGINT, stopListening)
  parser = argparse.ArgumentParser(description="Accept input either interactively or from an RFID reader")
  parser.add_argument("-input", choices=["interactive", "rfid"], help="Specify input type: 'interactive' or 'rfid'", required=False)
  parser.add_argument("-output", choices=["tty", "lcd","none"], help="Specify output type: 'tty' or 'lcd' or 'none'", required=False)
  args = parser.parse_args()
  if args.input != None:
    inputMode = args.input
  if args.output != None:
    outputMode = args.output

  mixer.init()

  drive = Drive()
  drive.mountDrive()
  while ( not stop and playNextSong(drive)):
    pass