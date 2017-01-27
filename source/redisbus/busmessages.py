import json
import datetime

class BusMessage:
  def __init__(self, messageType, payload):
    if not type(messageType) is str:
      raise Exception('messageType must be a string')
    self.messageType = messageType
    self.payload = payload

class _bus_message_binding():
  messageType = ""

class BusMessageSerialiser():
  def serialise(self, message):
    if not type(message) is BusMessage:
      raise Exception('message must be a BusMessage object')
    binding = {
      "type": message.messageType,
      "timestamp" : datetime.datetime.utcnow().isoformat(),
      "payload" : message.payload      
      }
    return json.dumps(binding)