import yaml
import os

class SongNotFound(Exception):
    pass


def loadConfig(filepath,mountpoint):
  # Load YAML data from file
  with open(mountpoint + "/" + filepath, 'r') as file:
    yaml_data = yaml.safe_load(file)
    print(yaml_data)
    return findSongs(yaml_data,mountpoint)

def findSongs(data,mountpoint):
  for song in data:
    if not os.path.exists(mountpoint + "/music/"+data[song]):
      raise SongNotFound("song not found: " + data[song])
  return data

if __name__ == "__main__":
  if loadConfig("config.yml","../usb"):
    print("pass")
  else:
    print("fail")