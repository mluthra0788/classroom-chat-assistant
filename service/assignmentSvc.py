from googleapiclient.discovery import build

def get_service(creds):
    return build('classroom', 'v1', credentials=creds)

def get_student_assignments(service):
    results = service.courses().list().execute()
    assignments = []
    for course in results.get('courses', []):
        coursework = service.courses().courseWork().list(courseId=course['id']).execute()
        for work in coursework.get('courseWork', []):
            assignments.append({
                'course': course['name'],
                'title': work['title'],
                'due': work.get('dueDate', 'N/A')
            })
    return assignments

def create_assignment(service, course_id, title, description, due_date):
    coursework = {
        'title': title,
        'description': description,
        'workType': 'ASSIGNMENT',
        'state': 'PUBLISHED',
        'dueDate': due_date
    }
    return service.courses().courseWork().create(courseId=course_id, body=coursework).execute()
