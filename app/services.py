import subprocess, sys, os, time, csv, operator

#ffm_path = "app/model/ffm/"
ffm_path = "model/ffm/"

NR_THREAD = 3
mentor_profiles = []
mentor_header = 'mentorId,mentorGender,mentorEducation,mentorLocation,mentorTitle,mentorSkillsets'.split(',')


def read_mentor_profiles(mentor_input):

	mentor_profiles = []
	with open(mentor_input, 'r') as mentor_f:
		reader = csv.reader(mentor_f, delimiter=',')
		for row in reader:
			mentor_profile = row[0].strip().split(',')
			mentor_profiles.append(mentor_profile)
            #test_list.append(user_profile + mentor_profile)
	return mentor_profiles

def create_test_prediction(user_profile):

	test_list = []
	mentor_profiles = read_mentor_profiles(ffm_path + 'data/mentor_profile.csv')
	#print mentor_profiles
	for mentor_profile in mentor_profiles:
		test_list.append(user_profile + mentor_profile)

	#print test_list

	header = ['Label'] + ['C' + str(i + 1) for i in range(len(test_list[0]))]
	# print header
	with open(ffm_path + 'te.csv', 'wb') as test_f:
		writer = csv.writer(test_f, delimiter=',')
		writer.writerow(header)
		for item in test_list:
			writer.writerow(item)
'''
user_profile: dictionary of user profile
k: specify numbers of recommendation
 
'''	
def getRecommendation(user_profile, k):

	# ===== Create test set csv
	create_test_prediction(user_profile)

    # Something should be improved for this ffm transformation
	# ===== Transform csv to ffm and do prediction by model
	cmd_transformation = '{ffm_path}converters/parallelizer-b.py -s {nr_thread} {ffm_path}/converters/pre-b.py {ffm_path}te.csv {ffm_path}te.ffm'.format(ffm_path=ffm_path, nr_thread=NR_THREAD)
	subprocess.call(cmd_transformation, shell=True)

	cmd_prediction = './{ffm_path}ffm-predict {ffm_path}te.ffm {ffm_path}/model {ffm_path}out_te.csv'.format(ffm_path, ffm_path=ffm_path)
	subprocess.call(cmd_prediction, shell=True)

	# example of result_list: [0.91, 0.93, 0.95, 0.92, 0.90]
	# turn result_list to result_dic = {0:0.91, 1:0.93, 2:0.95, 3:0.92, 4:0.90}
	result = {}
	with open(ffm_path + 'out_te.csv', 'r') as out_f:
		reader = csv.reader(out_f, delimiter=',')
		for i, row in enumerate(reader):
			result[i] =float(row[0])

	sorted_result = sorted(result.items(), reverse=True, key=operator.itemgetter(1))
	print sorted_result

    recommended_mentors = []
    for i in range(k):
        recommended_mentor_id = sorted_result[i][0]
        recommended_mentor_info = mentor_profiles[recommended_mentor_id]
        # print recommended_mentor_info
        recommended_mentor_profile = {}
        # feature: info for feature in mentor_header and for info in recommended_mentor_info[recommended_mentor_id]
        for idx in range(len(mentor_header)):
            key = mentor_header[idx]
            value = mentor_profiles[recommended_mentor_id][idx]
            recommended_mentor_profile[key] = value
        recommended_mentors.append(recommended_mentor_profile)

    return recommended_mentors

if __name__ == "__main__":
	
	
	test_user = ["0", "female", "highschool", "WA", "IP/SDN/AfterEffect/TCP/IaaS/"]
	out = getRecommendation(test_user, 5)