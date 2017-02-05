import picamera
from io import BytesIO
import time
from datetime import datetime
import threading
import os

class InMemoryCaptureEngine:
  def __init__(self, **kwargs):
    # Settings
    self._captureInterval = kwargs.get('captureInterval', 2)
    self._reporter = kwargs.get('reporter', None)
    self._cameraSettings = kwargs.get("cameraSettings", {})

    # Initialisation
    self._stopSignal = threading.Event()
    self._thread = None
    self._lastImage = None

  def start(self):
    if self._thread is None:
      cam = picamera.PiCamera()
      settings = self._cameraSettings
      self._camera = cam
      
      # Settings
      cam.resolution = settings.get("resolution", (640, 480))
      
      self._thread = threading.Thread(target=self._captureloop)
      self._thread.start()

  def stop(self):
    self._stopSignal.set()
    self._thread = None

  def _captureloop(self):
    while not self._stopSignal.is_set():
      #timeStamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
      
      with BytesIO() as stream:
        self._camera.capture(stream, 'jpeg')
        stream.seek(0)
        self._report(stream)
        
      self._stopSignal.wait(self._captureInterval)
    self._camera.close()

  def _report(self, imageStream):
    if not self._reporter is None:
      self._reporter(imageStream.getvalue())