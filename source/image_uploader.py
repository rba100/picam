import storage
import messagebus
import os

class SubscribingUploader:
  def __init__(self):
    self._uploader = storage.S3Storage(bucketName = "rba-picam")
    self._serialiser = messagebus.BusMessageSerialiser()
    self._s3Folder = "images"

  def start(self):
    self._subscriber = messagebus.RedisbusSubscriber("localhost", 6379)
    self._subscriber.open('picam', self._handler)

  def stop(self):
    self._subscriber.close()

  def _handler(self, rawMessage):
    message = self._serialiser.deserialise(rawMessage)
    if message.messageType == "image-saved":      
      filePath = message.payload["fileName"]
      print("Uploading: " + str(filePath))
      localFolder, fileName = os.path.split(filePath)
      targetPath = os.path.join(self._s3Folder, fileName).replace("_","/")
      self._uploader.move(filePath, targetPath)
