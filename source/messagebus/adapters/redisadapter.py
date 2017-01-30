import redis

class RedisbusPublisher:
  def __init__(self, host, port):
    self._host = host
    self._port = port

  def open(self):
    self._r = redis.StrictRedis(host=self._host, port=self._port)
  
  def close(self):
    pass #do nothing, redis object does not require disposal
  
  def publish(self, channelName, payload):
    self._r.publish(channelName, payload)
    
class RedisbusSubscriber:
  def __init__(self, host, port):
    self._host = host
    self._port = port

  def _handler(self, message):
    self._innerHandler(message["data"])

  def open(self, channelName, handler=None):
    self._innerHandler = handler
    self._r = redis.StrictRedis(host=self._host, port=self._port)
    self._p = self._r.pubsub(ignore_subscribe_messages=True)
    self._p.subscribe(**{channelName: self._handler})
    self._thread = self._p.run_in_thread(sleep_time=0.001)
    
  def close(self):
    self._thread.stop()
    self._p.close()
