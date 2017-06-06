from datetime import datetime

def tally(service, course_id, assignment_dict):

	try:

		result = service.courses().courseWork().studentSubmissions().list(
			courseId=course_id,
			courseWorkId='-',
			pageSize=20
			).execute()

	except:

		# let HTTP 404 errors pass silently
		pass

	utcnow = datetime.utcnow()

	today = datetime(utcnow.year, utcnow.month, utcnow.day)

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

			try:

				assignment_dict[submission['id']] = submission['state']

			except KeyError:

				assignment_dict[submission['id']] = submission['state']

	return len(assignment_dict)
