import picamera
import time
from datetime import datetime
import threading
import os

class CaptureEngine:
  def __init__(self, **kwargs):
    # Settings
    self._targetFolder = kwargs.get('targetFolder','')
    self._captureInterval = kwargs.get('captureInterval', 2)
    self._reporter = kwargs.get('reporter', None)
    self._cameraSettings = kwargs.get("cameraSettings", {})

    # Initialisation
    self._stopSignal = threading.Event()
    self._thread = None

  def start(self):
    if self._thread is None:
      self._camera = picamera.PiCamera()
      self._thread = threading.Thread(target=self._captureloop)
      self._thread.start()

  def stop(self):
    self._stopSignal.set()
    self._thread = None

  def _captureloop(self):
    while not self._stopSignal.is_set():
      fileName = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S") + ".jpeg"
      filePath = os.path.join(self._targetFolder, fileName)
      self._camera.capture(filePath)
      self._report(filePath)
      self._stopSignal.wait(self._captureInterval)
    self._camera.close()

  def _report(self, filePath):
    if not self._reporter is None:
      self._reporter(filePath)