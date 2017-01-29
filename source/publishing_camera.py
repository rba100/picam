import captureengine
import messagebus

class PublishingCamera:
  def __init__(self, **kwargs):
    self._redisHost = kwargs.get("redisHost", "localhost")
    self._redisPort = kwargs.get("redisPort", 6379)
    self._targetFolder = kwargs.get("targetFolder","/home/pi/dump")
    self._captureInterval = kwargs.get("captureInterval", 2)
    self._busMessageSerialiser = messagebus.BusMessageSerialiser()
    pass
  
  def _reporter(self, fileName):
    message = messagebus.BusMessage('image-captured',{ "fileName": fileName })
    serialised = self._busMessageSerialiser.serialise(message)
    self._publisher.publish('picam', serialised)
    pass
  
  def start(self):
    self._publisher = messagebus.RedisbusPublisher(self._redisHost, self._redisPort)
    self._publisher.open()
    self._captureEngine = captureengine.CaptureEngine(targetFolder = self._targetFolder,
                                        captureInterval = self._captureInterval,
                                        reporter = self._reporter)
    self._captureEngine.start()
    
  def stop(self):
    self._captureEngine.stop()
    self._publisher.close()
