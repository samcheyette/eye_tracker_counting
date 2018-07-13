import copy
import csv
import pandas
import os

subdir = "discrimination"

files = os.listdir("/home/sam/Documents/eye_tracker_counting/data/%s" % subdir)
out_file = "discrimination_tracker_data.csv"

p = 0
t = 0
header = []
data = ""
names = []

for name in files:
	if ".tsv" in name:
		names.append("discrimination_" + name.replace(".tsv", ".csv"))
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



out_file = "discrimination_response_data.csv"

p = 0
t = 0
first = False
header = []
data = ""
for name in names:

	if (".csv" in name and "tracker" not in name and "1" in name and
		 out_file[16:] not in name):
		file = open("%s/%s" % (subdir,name), "r")
		l = file.readline()
		last_trial = ''
		while l != "":
			r = l.replace("\n", "").split(",")
			l = file.readline()

			t1 = r[3]
			t2 = r[4]
			n1 = r[7]
			n2 = r[8]

			

			if "Subject" in r[0]:
				header = "pid\ttrial_id\tdir\t" + "\t".join(r) + "\n"
				#header = "pid\ttrial_id\t" + "\t".join(r) + "\n"

			else:

				if r[2] != last_trial:
					t += 1
					last_trial = r[2]


				#if t1 != t2 and float(t1) > float(t2):
					#r = (r[0:3] + r[3:5][::-1] + r[5:7] + 
						#	r[7:9][::-1] + [str(2-(int(r[9])-1))] + r[10:])


				newl = "%d\t%d\t%s\t" % (p, t, t1)
				newl += "\t".join(r)
				data += newl + "\n"

		p += 1


data = header + data
f = open(out_file, "w+")
f.write(data)
f.close()
