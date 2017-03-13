from __future__ import print_function 
import httplib2

import pprint
from apiclient import discovery

from auth import get_credentials

from datetime import datetime

def main():

	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('classroom', 'v1', http=http)

	while True:
		result = service.courses().courseWork().studentSubmissions().list( 
			courseId=1644278098,  
			courseWorkId='-',
			fields='studentSubmissions(updateTime,state)'
			).execute()

		utcnow = datetime.utcnow()

		today = datetime(utcnow.year, utcnow.month, utcnow.day)

		counter = 0

		for submission in result['studentSubmissions']:

			year = int(submission['updateTime'][0:4])

			month = int(submission['updateTime'][5:7])

			day = int(submission['updateTime'][8:10])

			hour = int(submission['updateTime'][11:13])

			minute = int(submission['updateTime'][14:16])

			subtime = datetime(year, month, day, hour, minute)

			if ((subtime > today) and 
			(submission['state'] == "RETURNED" or
			 submission['state'] == "TURNED_IN")):
				counter += 1

		print(counter)
		
if __name__ == '__main__':
    main()
