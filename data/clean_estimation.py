import copy
import csv
import pandas
import os

subdir = "estimation"

files = os.listdir("/home/sam/Documents/eye_tracker_counting/data/%s" % subdir)
out_file = "estimation_tracker_data.csv"

p = 0
t = 0
header = []
data = ""
names = []

for name in files:
	if ".tsv" in name:
		names.append(name.replace(".tsv", ".csv"))
		file = open("%s/%s" % (subdir,name), "r")
		l = file.readline()
		while l != "":
			r = l.replace("\n","").split("\t")
			r = [x for x in r if x != '']
			if len(r) > 3:
				if ('Time' in r[0] and 'Event' in r[len(r)-1]):
					header = "pid\t" + "trial_id\t" + "\t".join(r[:-1])[:-1] + "\n"
				else:
					if r[0] == '0.0' or r[0] == '0':
						t += 1
					if t < 3:
						print r
					newl = "%d\t%d\t" % (p, t)
					newl += "\t".join(r)[:-1]
					data += newl + "\n"

			l = file.readline()

		p += 1
		file.close()
print header

data = header + data
f = open(out_file, "w+")
f.write(data)
f.close()



out_file = "estimation_response_data.csv"

p = 0
t = 0
first = False
header = []
data = ""
for name in names:

	if (".csv" in name and "tracker" not in name and "1" in name and
		 out_file[:5] not in name):
		file = open("%s/%s" % (subdir,name), "r")
		l = file.readline()
		last_trial = ''
		while l != "":
			r = l.replace("\n", "").split(",")
			l = file.readline()

			if "Subject" in r[0]:
				header = "pid\ttrial_id\t" + "\t".join(r) + "\n"

			else:
				if r[2] != last_trial:
					t += 1
					last_trial = r[2]

				newl = "%d\t%d\t" % (p, t)
				newl += "\t".join(r)
				data += newl + "\n"

		p += 1


data = header + data
f = open(out_file, "w+")
f.write(data)
f.close()
