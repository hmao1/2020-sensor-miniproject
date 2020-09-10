import json
import statistics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




tem_list=[]
occu_list=[]
room_list=[]
with open('sensor.txt','r') as file:
	for line in file:
		#check the non-empty line
		if line!="\n":
			#convert data line to dictionary and store in res
			res=json.loads(line)
			head_str=next(iter(res))

			tem_list.append((res[head_str]['temperature'])[0])
			occu_list.append((res[head_str]['occupancy'])[0])
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




#plot the probability distribution
x=np.arange(len(uniq_room))
plt.bar(x,uniq_percent)
plt.xticks(x,uniq_room)
plt.xlabel('sensor in rooms')
plt.ylabel('probability')
plt.title('sensor type probability distribution')
plt.show()



#logic to capture the abnormal temperature point



