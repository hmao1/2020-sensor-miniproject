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

			



#for temperature
print("total data points: "+str(len(tem_list)) )
print("mean of temperature: "+str(statistics.mean(tem_list)))
print("variance of temperature: "+str(statistics.variance(tem_list)))

#for occupation
print("mean of occupancy: "+str(statistics.mean(occu_list)))
print("variance of occupancy: "+str(statistics.variance(occu_list)))


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





#logic to capture the abnormal temperature point
std1=statistics.pstdev(tem_list)
print("The first standard deviation temperature "+str(std1))



