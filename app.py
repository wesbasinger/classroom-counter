from __future__ import print_function 
from time import sleep
import httplib2

from apiclient import discovery

from auth import get_credentials
from counter import tally

from Adafruit_LED_Backpack import SevenSegment
from gpiozero import Buzzer

display = SevenSegment.SevenSegment()
buzzer = Buzzer(17)

display.begin()

colon = False

courses = [1644100493, 1644278098]

def main():

	# initialize display during boot
	display.clear()
	display.print_number_str("0000")
	display.write_display()

	# 40 second delay for network to come up during auto start at boot
	sleep(40)


	global_count = 0

	print("Attempting to get credentials...")

	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('classroom', 'v1', http=http)

	print("Credentials seem to have been obtained...")

	print("Application is now running...")

	while True:

		combined_count = 0

		for course in courses:

			combined_count += tally(service, course)

		if combined_count != global_count:

			buzzer.on()
			sleep(0.40)
			buzzer.off()
			global_count = combined_count
			
		display.clear()

		display.print_number_str(
			str(combined_count)
		)

		display.write_display()
		
if __name__ == '__main__':
    main()
