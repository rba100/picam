from PIL import Image

class ImageDifferentiator:
  def __init__(self, **kwargs):
    # Settings
    self._mode = "RGB"
    self._cameraSettings = kwargs.get("cameraSettings", {"resolution": (640,480)})
    self._regionSize = 10
    self._threshhold = kwargs.get("motionThreshold", 10)
    self._regionThreshhold = kwargs.get("motionRegionThreshold", 20)

    # Initialisation    
    self._last = None
    self._current = None

  def push(self, imageBytes):
    if not self._last is None:
      self._last.close()      
    self._last = self._current
    self._current = Image.frombuffer(self._mode, self._cameraSettings["resolution"], imageBytes);    

  def isDifferent(self):
    if self._last is None or self._current is None:
      return False
    rLast = self._regionalise(self._last)
    rCurr = self._regionalise(self._current)
    return self._compRegions(rLast, rCurr)

  def save(self, fileName):
    if not self._current is None:
      self._current.save(fileName)

  def _compRegions(self, left, right):
    regionsX, regionsY = int(len(left) / self._regionSize), int(len(left[0]) / self._regionSize)
    hits = 0
    for rx in range(regionsX):
      for ry in range(regionsY):
        if abs(left[rx][ry] - right[rx][ry]) >= self._threshhold:
          hits += 1
          if hits >= self._regionThreshhold:
            return True
    return False

  def _regionalise(self, image):
    maxX, maxY = image.size
    regionsX, regionsY = int(maxX / self._regionSize), int(maxY / self._regionSize)    
    regionMap = [[0] * regionsY] * regionsX
    
    pixels = image.convert(mode='L').resize((regionsX, regionsY)).getdata(0)
    rx = 0
    ry = 0
    for pixelValue in pixels:
      regionMap[rx][ry] += pixelValue            
      rx += 1
      if rx == regionsX:
        rx = 0      
        ry += 1

    return regionMap