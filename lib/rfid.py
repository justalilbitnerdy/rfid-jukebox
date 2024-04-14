
import RPi.GPIO as GPIO
import lib.dependencies.MFRC522python.MFRC522 as MFRC522
import signal

# function to read uid an conver it to a string
def uidToString(uid):
  mystring = ""
  for i in uid:
    mystring = format(i, '02X') + mystring
  return mystring

class RFIDReader:
  continue_reading = True
  

  # Capture SIGINT for cleanup when the script is aborted
  def end_read(self,signal, frame):
    print("Ctrl+C captured, ending read.")
    self.continue_reading = False
    GPIO.cleanup()

  # Create an object of the class MFRC522
  MIFAREReader = MFRC522.MFRC522()

  def getNextID(self):
    uid = None
    while uid == None:
      # Scan for cards
      (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
      # If a card is found
      if status == self.MIFAREReader.MI_OK:
        # Get the UID of the card
        (status, uid) = self.MIFAREReader.MFRC522_SelectTagSN()
        # If we have the UID, continue
        if status == self.MIFAREReader.MI_OK:
          uid = uidToString(uid)
          if type(uid) is list:
            continue
    return uid
if __name__ == "__main__":
  reader = RFIDReader()
  print(reader.getNextID())