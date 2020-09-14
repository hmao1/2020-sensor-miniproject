import json
import statistics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


time_list=[]
tem_list=[]
occu_list=[]
co2_list=[]

room_list=[]
office_temp=[]
office_occu=[]


with open('sensor.txt','r') as file:
	for line in file:
		#check the non-empty line
		if line!="\n":
			#convert data line to dictionary and store in res
			res=json.loads(line)
			head_str=next(iter(res))

			tem_list.append((res[head_str]['temperature'])[0])
			occu_list.append((res[head_str]['occupancy'])[0])
			co2_list.append((res[head_str]['co2'])[0])
			time_list.append((res[head_str]['time']))
			room_list.append(head_str)

			

"""
 For the part that displays the mean and variance of temperature and occupation, I changed the format.
 Keep 5 significant digits.
 No essential algorithm change.
"""

#for temperature
print("\ntotal data points: {} \n".format(len(tem_list)))
print("mean of temperature: {:.5} \n".format(statistics.mean(tem_list)))
print("variance of temperature: {:.5} \n".format(statistics.variance(tem_list)))

#for occupation
print("mean of occupancy: {:.5} \n".format((statistics.mean(occu_list))))
print("variance of occupancy:{:.5} \n".format((statistics.variance(occu_list))))



#for probability distribution of different type of sensor
uniq_room=[]
uniq_percent=[]
size_total=len(room_list)

for room in room_list:
	if room not in uniq_room:
		uniq_room.append(room)

for uniq in uniq_room:
	uniq_percent.append((room_list.count(uniq))/size_total)

print(uniq_percent)


#plot probability density for sensor type
#temperature
fig=plt.figure()

plt.subplot(2,2,1)
plt.title('probability distribution function')

s1=pd.Series(tem_list)
ax1=s1.plot.kde()
plt.xlabel('temperature')
plt.ylabel('probability')

#occupancy
plt.subplot(2,2,2)
s2=pd.Series(occu_list)
ax2=s2.plot.kde()
plt.xlabel('occupancy')
plt.ylabel('probability')

#co2
plt.subplot(2,2,3)
s3=pd.Series(co2_list)
ax3=s3.plot.kde()
plt.xlabel('co2')
plt.ylabel('probability')

plt.show()


"""
For the 3rd part of the mini-project:
1) find out the standard deviation
2) run a loop go thought the whole list
3) find out all the "bad data" and store into a list
4) store "good data" into a new list
5) use the length of "bad data" list to calculate the bad data percentage
6) use the new list of good data to calculate the new standard deviation
"""

#logic to capture the abnormal temperature point
std1=statistics.pstdev(tem_list)
print("The first standard deviation temperature {:.5}".format(str(std1)))

#one list to store good data and another for bad data
temp_good = []
temp_bad = []

for check in tem_list:
	if ((check-statistics.mean(tem_list))>=std1*3):
		temp_bad.append(check)
	else:
		temp_good.append(check)

print ("Here are the bad points: ",end="")
for i in temp_bad:
	print ("{:.5} ".format(float(i)),end="")

print ("\n The standard deviation without \'bad data\' is: {:.5f}".format(statistics.pstdev(temp_good)))


print("{}".format(len(temp_bad)))
print("{}".format(len(temp_good)))
print("{}".format(len(temp_bad)+len(temp_good)))


