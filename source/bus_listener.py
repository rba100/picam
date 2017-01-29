import messagebus
import time

def printer(message):
  print(message)

subscriber = messagebus.RedisbusSubscriber("localhost", 6379)
print("Opening connection...")
subscriber.open('image-captured', printer)
try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  print("Closing connection...")
  subscriber.close()