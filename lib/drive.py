import os
from lib.config import loadConfig
from datetime import datetime

mountpoint = "/etc/jukebox/usb"
class Unmounted(Exception):
    pass
class SongNotFound(Exception):
    pass


class Drive:
  config = None
  def __init__(self):
    self.config = None

  def mountDrive(self):
    # mount drive
    # listen for drive force unplugged?
    configFile = os.path.normpath(os.path.join(mountpoint, "config.yml"))
    self.config = loadConfig("config.yml",mountpoint)
    pass

  def unmountDrive(self):
    #unmount drive
    self.config = None
    pass

  def getSong(self,songID):
    self.mountedCheck()
    if songID in self.config:
      return os.path.normpath(os.path.join(mountpoint, "music/", self.config[songID]))
    self.logNewID(songID)
    return None
  
  def logNewID(self,songID):
    cardsLog = os.path.normpath(os.path.join(mountpoint, "newCards.txt"))
    with open(cardsLog, 'a') as file:
      # Get the current time
      current_time = datetime.now()
      # Format the current time in a human-readable format
      formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
      # Append the formatted time to the file
      file.write(f"{formatted_time} - " + str(songID) + "\n")

  def mountedCheck(self):
    if self.config == None:
      raise Unmounted("Drive unmounted")
