import redis

class redis_publisher:
  def __init__(self, host, port):
    self.host = host
    self.port = port

  def open(self):
    self.r = redis.StrictRedis(host=self.host, port=self.port)
  
  def close(self):
    pass #do nothing, redis object does not require disposal
  
  def publish(self, channelName, payload):
    r.publish(channelName, payload)
    
class redis_subscriber:
  def __init__(self, host, port):
    self.host = host
    self.port = port

  def open(self, channelName, handler=None):
    self.r = redis.StrictRedis(host=self.host, port=self.port)
    self.p = r.pubsub(ignore_subscribe_messages=True)
    self.p.subscribe(**{channelName: handler})
    
  def close(self):
    self.p.close()