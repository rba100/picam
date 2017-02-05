import captureengine
import messagebus

class MotionTriggeredPublishingCamera:
  def __init__(self, **kwargs):
    # Settings
    self._redisHost = kwargs.get("redisHost", "localhost")
    self._redisPort = kwargs.get("redisPort", 6379)
    self._targetFolder = kwargs.get("targetFolder","/home/pi/dump")
    self._captureInterval = kwargs.get("captureInterval", 2)
    self._cameraSettings = kwargs.get("cameraSettings", {})
    self._motionThreshold = kwargs.get("motionRegionThreshold", 10)
    self._motionRegionThreshold = kwargs.get("motionRegionThreshold", 20)
    
    # Initialisation
    self._busMessageSerialiser = messagebus.BusMessageSerialiser()    
    self._imageDiffer = captureengine.ImageDifferentiator()
  
  def _reporter(self, imageBytes):
    self._imageDiffer.push(imageBytes)
    if self._imageDiffer.isDifferent():
      #timeStamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
      #fileName = timeStamp + ".jpeg"
      print("MOTION")
      #self._imageDiffer.save(fileName)
    else:
      print("nothing")
    
    #message = messagebus.BusMessage('image-captured', { "fileName": fileName })
    #serialised = self._busMessageSerialiser.serialise(message)
    #self._publisher.publish('picam', serialised)
    pass
  
  def start(self):
    self._publisher = messagebus.RedisbusPublisher(self._redisHost, self._redisPort)
    self._publisher.open()
    self._captureEngine = captureengine.InMemoryCaptureEngine(
                                        captureInterval = self._captureInterval,
                                        cameraSettings = self._cameraSettings,
                                        reporter = self._reporter)
    self._captureEngine.start()
    
  def stop(self):
    self._captureEngine.stop()
    self._publisher.close()