import json
import datetime

class BusMessage:
  def __init__(self, messageType, payload):
    if not type(messageType) is str:
      raise Exception('messageType must be a string')
    self.messageType = messageType
    self.payload = payload
    self.timestamp = None
  def __str__(self):
    if self.timestamp is None:
      ts = ")"
    else:
      ts = " : " + self.timestamp + ")"
    return "(" + self.messageType + " : " + str(self.payload) + ts

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

  def deserialise(self, jsonString):
    if not type(jsonString) is str:
      raise Exception('deserialise() must be called with a string argument')
    deserialised = json.loads(jsonString)
    if not type(deserialised) is dict:
      raise Exception("'" + jsonString + "' could not be deserialised as a dictionary")
    message = BusMessage(deserialised["type"], deserialised["payload"])
    message.timestamp = deserialised["timestamp"]
    return message
