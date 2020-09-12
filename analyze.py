#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np
import statistics



def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}
         

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)
       

    #calulate the mean, variance
    #print("total data points for lab1: "+ str(len(data['temperature']['lab1'])))
    print("the median of lab1 temperature is: "+str(np.nanmedian(data['temperature']['lab1'])))
    print("the variance of lab1 temperature is: "+str(np.var(data['temperature']['lab1'])))
    print("the median of lab1 occupancy is: " +str(np.nanmedian(data['occupancy']['lab1'])))
    print("the variance of lab1 occupancy is: "+str(np.var(data['occupancy']['lab1'])))
    

    # #plot the data (given) 
    # for k in data:
    #     data[k].plot()
    #     time = data[k].index
    #     data[k].hist()
    #     plt.figure()
    #     plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
    #     plt.xlabel("Time (seconds)")

    # plt.show()

    
    #access the index(time) for time interval
    
    for k in data:
        time0=data[k].index

    interval=(np.diff(time0.values).astype(np.float64) // 1000000000)
   
    



    print("the mean of time interval is: "+str(np.mean(interval)) +"ms")
    print("the median of time interval is: "+str(np.var(interval))+'ms')

    
    #######plot data
    fig=plt.figure()


    plt.subplot(2,2,1)
    plt.title('probability distribution function for lab1')

    s1=pandas.Series(data['temperature']['lab1'])
    ax1=s1.plot.kde()
    plt.xlabel('temperature')
    plt.ylabel('probability')




    #occupancy
    plt.subplot(2,2,2)
    s2=pandas.Series(data['occupancy']['lab1'])
    ax2=s2.plot.kde()
    plt.xlabel('occupancy')
    plt.ylabel('probability')



    #co2
    plt.subplot(2,2,3)
    s3=pandas.Series(data['co2']['lab1'])
    ax3=s3.plot.kde()
    plt.xlabel('co2')
    plt.ylabel('probability')


    #time
    plt.subplot(2,2,4)
    s4=pandas.Series(interval)
    ax4=s4.plot.kde()
    plt.xlabel('time interval in ms')
    plt.ylabel('probability')


    plt.show()



    #print(interval)


    #########detect abnormal temperature
    mean_tem_lab1=np.mean(data['temperature']['lab1'])
    print("tem mean lab1: "+str(mean_tem_lab1))
    std1=np.std(data['temperature']['lab1'])
    std2=2*std1
    std3=3*std1

    ab_tem1=[]
    ab_tem2=[]
    lab1_tem=data['temperature']['lab1']
  

    
    for i in lab1_tem:
       if not ((mean_tem_lab1-std1) <= i <=(mean_tem_lab1+std1)):
            ab_tem1.append(i)
       elif not ((mean_tem_lab1-std2) <= i <=(mean_tem_lab1+std2)): 
            ab_tem2.append(i) 
       else:
            continue      

    #maybe better way to clean the abnormal data point 
    clean_ab_tem1=[x for x in ab_tem1 if str(x) != 'nan']
    clean_ab_tem2=[x for x in ab_tem2 if str(x) != 'nan']
    
    #count the total lab1 temperature received
    lab1_tem_count=0
    for i in lab1_tem:
        if str(i)!='nan':
            lab1_tem_count+=1



    #calculate the temperature median and variance regarding the abnormal data
    # for i in lab1_tem:
    #     if i==clean_ab_tem1[0]:
    #         print("exist!!")

    normal_tem1=[x for x in lab1_tem if (x not in clean_ab_tem1 and str(x)!='nan' )]
    
           


    print("the standard deviation of the temperature in lab1 is: "+str(std1))
    print("\n")
    print("lab1 temperature that one standard deviation away the mean: "+str(clean_ab_tem1))
    print("\n")
    print("two standard deviation away the mean: "+str(clean_ab_tem2))
    print("\n")
    print("the total number of lab1 temperature: "+str(lab1_tem_count))
    print("the percentage of bad lab1 temperature data points: "+ str(len(clean_ab_tem1)/float(lab1_tem_count)))
    print("\n")
    print("after removing the abnormal (one standard deviation away mean), the median is: "+str(np.median(normal_tem1)))
    print('\n')
    print("after removing the abnormal, the variance is: "+str(np.var(normal_tem1)))
    #print("the percent of bad data is: "+str(len(clean_ab_tem1))/float(len()))

        
       



