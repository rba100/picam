import storage
import messagebus

class SubscribingUploader:
  def __init__(self):
    self._uploader = storage.S3Storage(bucketName = "rba-picam")
    self._serialiser = messagebus.BusMessageSerialiser()

  def start(self):
    self._subscriber = messagebus.RedisbusSubscriber("localhost", 6379)
    self._subscriber.open('picam', self._handler)

  def close(self):
    self._subscriber.close()

  def _handler(self, rawMessage):
    print(rawMessage)
    message = self._serialiser.deserialise(rawMessage)
    if message.messageType == "image-captured":
      filePath = message.payload["fileName"]
      print("Uploading: " + str(filePath))
      self._uploader.move(filePath, filePath)
    else:
      print("Ignoring: " + message.messageType)
