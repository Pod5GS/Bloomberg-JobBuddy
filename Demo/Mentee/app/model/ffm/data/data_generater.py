from random import randint
import csv
menteeInterests = 'Python, Java, C++, C, C#, Objective-C, Ruby, Javascript, Swift, React, Angular, HTML, CSS, Photoshop, Illustrator, AfterEffect, Wireframing, RESTful APIs, Bootstrap, jQuery, Git, Flask, Datastrcutes and Algorithms, Operating System, Linux, Go, Perl, Unix, TCP, IP, SDN, NodeJS, XML, NoSQL, SOAP, REST APIs, GraphQL, UI, UX, CAD, CAM, PaaS, IaaS, Cloud, RFI, RFP, SQL'.split(', ')
titles = 'UX Designer, Front-End Software Engineer, Back-End Software Engineer, Mobile Software Engineer, Full Stack Software Engineer, Site Reliability Engineer, Quality Assurance Engineer, Enterprise Engineer, Product Engineer, Sales Engineer'.split(', ')
mentorSkills = {'UX Designer': 'HTML, CSS, Photoshop, Illustrator, AfterEffect, Wireframing', 'Front-End Software Engineer': 'HTML, CSS, Javascript, RESTful APIs, Bootstrap, jQuery, Angular, React, Git', 'Back-End Software Engineer': 'C, C++, Java, C#, Ruby, Python, Flask, Datastrcutes and Algorithms, Operating System, Linux, Git', 'Mobile Software Engineer': 'Java, C#, Objective-C, Swift', 'Full Stack Software Engineer': 'HTML, CSS, Javascript, RESTful APIs, Bootstrap, jQuery, Angular, React, Git, C, C++, Java, C#, Ruby, Python, Flask, Datastrcutes and Algorithms, Operating System, Linux', 'Site Reliability Engineer': 'C, C++, Java, Python, Go, Perl, Ruby, Unix, Linux, TCP, IP, SDN', 'Quality Assurance Engineer': 'HTML, CSS, XML, NodeJS, Angular, NoSQL', 'Enterprise Engineer': 'SOAP, REST APIs, GraphQL, React, Angular, UI, UX', 'Product Engineer': 'CAD, CAM', 'Sales Engineer': 'PaaS, IaaS, Cloud, RFI, RFP, SQL'}
gender = ['male', 'female']
location = ['NY', 'CA', 'TX', 'WA', 'NJ', 'GA', 'UT', 'AZ']
menteeeducation = ['highschool', 'bachelor']
mentoreducation = ['bachelor', 'master', 'phd']
count_mentee = 50
count_mentor = 10
rating_max = 10

def generate_fake_data():
	with open('validation.csv', 'wb') as f:
		header = 'mentorRating,menteeId,menteeGender,menteeEducation,menteeLocation,menteeInterests,mentorId,mentorGender,mentorEducation,mentorLocation,mentorTitle,mentorSkillsets\n'
		f.write(header)
		for menteeId in range(count_mentee):
			menteegender = gender[randint(0, 1)]
			menteeedu = menteeeducation[randint(0, 1)]
			menteelocation = location[randint(0, 7)]
			menteeinterests = ''
			for i in range(5):
				menteeinterests += menteeInterests[randint(0, 46)] + '/'
			for mentorId in range(count_mentor):
				mentorgender = gender[randint(0, 1)]
				mentoredu = mentoreducation[randint(0, 1)]
				mentorlocation = location[randint(0, 7)]
				mentortitle = titles[randint(0, 9)]
				skillset = mentorSkills[mentortitle].replace(', ', '/')
				rating = randint(0, rating_max)
				line = str(rating) + ',' + str(menteeId) + ',' + menteegender + ',' + menteeedu + ',' + menteelocation + ',' + menteeinterests + ',' + str(mentorId) + ',' + mentorgender + ',' + mentoredu + ',' + mentorlocation + ',' + mentortitle + ',' + skillset + '\n'
				f.write(line)
			
def generate_mentor_profile(count_mentor):

	with open('mentor_profile.csv', 'wb') as f:
		writer = csv.writer(f, delimiter=',')
		for mentorId in range(count_mentor):
			mentorgender = gender[randint(0, 1)]
			mentoredu = mentoreducation[randint(0, 1)]
			mentorlocation = location[randint(0, 7)]
			mentortitle = titles[randint(0, 9)]
			skillset = mentorSkills[mentortitle].replace(', ', '/')
			rating = randint(0, rating_max)
			line = str(mentorId) + ',' + mentorgender + ',' + mentoredu + ',' + mentorlocation + ',' + mentortitle + ',' + skillset + '\n'
			writer.writerow([line])
		
if __name__ == '__main__':
	generate_mentor_profile(count_mentor)
	