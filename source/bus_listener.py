import messagebus
import time

serialiser = messagebus.BusMessageSerialiser()

def printer(message):
  #deserialised = serialiser.deserialise(str(message["payload"]))
  #print(type(message))
  print(message)

subscriber = messagebus.RedisbusSubscriber("localhost", 6379)
print("Opening connection...")
subscriber.open('picam', printer)
try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  print("Closing connection...")
  subscriber.close()
