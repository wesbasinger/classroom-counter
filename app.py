from __future__ import print_function 
import httplib2

from apiclient import discovery

from auth import get_credentials
from counter import tally

from Adafruit_LED_Backpack import SevenSegment

display = SevenSegment.SevenSegment()

display.begin()

colon = False

courses = [1644100493, 1644278098]

def main():

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

		display.clear()

		display.print_number_str(
			str(combined_count)
		)

		display.write_display()
		
if __name__ == '__main__':
    main()
