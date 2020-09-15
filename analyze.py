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
       

    #calulate the mean, variance for temperature and occupation with 4 significant digits.
    print("for task2 part1 and 2\n")
    print("\nmedian of temperature in lab1 is: {:.5} \n".format( np.nanmedian(data['temperature']['lab1'])))
    print("variance of temperature in lab1 is: {:.5} \n".format(np.var(data['temperature']['lab1'])))
    print("median of occupancy in lab1 is: {:.5} \n".format(np.nanmedian(data['occupancy']['lab1'])))
    print("variance of occupancy in lab1 is: {:.5} \n".format(np.var(data['occupancy']['lab1'])))
   
    
    #calculate the time interval in second and store in interval_in_s
    for k in data:
        time0=data[k].index

    interval=(np.diff(time0.values).astype(np.float64) )
    interval_in_s=interval/1000000
    

    print("\nFor task2 part4\n")
    print("the mean of time interval for sensor is: {:.5}ms\n".format(np.mean(interval_in_s)))
    print("the variance of time interval is sensor is: {:.5}\n".format(np.var(interval_in_s)))
   
    
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
    s4=pandas.Series(interval_in_s)
    ax4=s4.plot.kde()
    plt.xlabel('time interval in ms')
    plt.ylabel('probability')


    plt.show()
    



    #########detect abnormal temperature
    """
    Basically, the algorithm will calculate the mean and standard deviation of
    the given data point. And check if each data point in range of first, second or
    third standard deviation 

    """
    mean_tem_lab1=np.mean(data['temperature']['lab1'])
    print("For lab1, the mean temperature is: {:.5}\n ".format(mean_tem_lab1))
    std1=np.std(data['temperature']['lab1'])
    std2=2*std1
    std3=3*std1

    ab_tem1=[]
    ab_tem2=[]
    ab_tem3=[]

    lab1_tem=data['temperature']['lab1']
    

    
    for i in lab1_tem:
       if not ((mean_tem_lab1-std1) <= i <=(mean_tem_lab1+std1)):
            ab_tem1.append(i)
       elif not ((mean_tem_lab1-std2) <= i <=(mean_tem_lab1+std2)): 
            ab_tem2.append(i) 
       elif not ((mean_tem_lab1-std3) <= i <=(mean_tem_lab1+std3)): 
            ab_tem3.append(i)
       else:
            continue      

    #maybe better way to clean the abnormal data point 
    clean_ab_tem1=[x for x in ab_tem1 if str(x) != 'nan']
    clean_ab_tem2=[x for x in ab_tem2 if str(x) != 'nan']
    clean_ab_tem3=[x for x in ab_tem3 if str(x) != 'nan']
    #count the total lab1 temperature received
    lab1_tem_count=0
    for i in lab1_tem:
        if str(i)!='nan':
            lab1_tem_count+=1

    ##need to check clean_ab_tem1 is not empty!!! so include and clean_ab_tem1.....2.....3
    normal_tem1=[x for x in lab1_tem if (x not in clean_ab_tem1 and str(x)!='nan' ) and clean_ab_tem1]
    normal_tem2=[x for x in lab1_tem if (x not in clean_ab_tem2 and str(x)!='nan' ) and clean_ab_tem2]
    normal_tem3=[x for x in lab1_tem if (x not in clean_ab_tem3 and str(x)!='nan' ) and clean_ab_tem3]      


    print("the standard deviation of the temperature in lab1 is {:.5}\n: ".format(std1))

    print("lab1 temperature that one standard deviation away the mean: "+str(clean_ab_tem1)+"\n")
    
    print("data points that two standard deviation away the mean: "+str(clean_ab_tem2)+"\n")
    
    print("data points three standard deviation away the mean: "+str(clean_ab_tem3)+"\n")

    print("the total number of lab1 temperature: "+str(lab1_tem_count)+"\n")


    if normal_tem1:
        print("Considering the data point ONE standard away mean as bad data point, then:")
        print("the percentage of bad lab1 temperature data points: {:.4}\n".format(str(len(clean_ab_tem1)/float(lab1_tem_count))))
        print("after removing the abnormal (1 standard deviation away mean), the median is: {:.5}\n ".format(np.median(normal_tem1)))
        print("after removing the abnormal (1 standard deviation away mean), the variance is: {:.5}\n ".format(np.var(normal_tem1)))
    
    
    if normal_tem2:
        print("Considering the data point TWO standard away mean as bad data point, then:")
        print("the percentage of bad lab1 temperature data points: {:.4}\n".format(str(len(clean_ab_tem2)/float(lab1_tem_count))))
        print("after removing the abnormal (2 standard deviation away mean), the median is: {:.5}\n ".format(np.median(normal_tem2)))
        print("after removing the abnormal (2 standard deviation away mean), the variance is: {:.5}\n ".format(np.var(normal_tem2)))
    
        
       
    if normal_tem3:
        print("\nConsidering the data point THREE standard away mean as bad data point, then:")
        print("the percentage of bad lab1 temperature data points: {:.4}\n".format(str(len(clean_ab_tem3)/float(lab1_tem_count))))
        print("after removing the abnormal (2 standard deviation away mean), the median is: {:.5}\n ".format(np.median(normal_tem3)))
        print("after removing the abnormal (2 standard deviation away mean), the variance is: {:.5}\n ".format(np.var(normal_tem3)))
    

    mean_tem_office=np.mean(data['temperature']['office'])
    mean_tem_class1=np.mean(data['temperature']['class1'])
    std3_tem_office=np.std(data['temperature']['office'])
    std3_tem_class1=np.std(data['temperature']['class1'])
    print("for task3 part3:according to the data point collected and considering temperature in 3 standard deviation away the mean are possible, then:")
    print("the possible bounds on temperature for lab1 is from {low} to {high}\n".format(low=round(mean_tem_lab1-std3,4),high=round(mean_tem_lab1+std3,4)))
    print("the possible bounds on temperature for office is from {low} to {high}\n".format(low=round(mean_tem_office-std3_tem_office,4),high=round(mean_tem_office+std3_tem_office,4)))
    print("the possible bounds on temperature for class1 is from {low} to {high}\n".format(low=round(mean_tem_class1-std3_tem_class1,4),high=round(mean_tem_class1+std3_tem_class1,4)))


    if normal_tem1:
        std3_lab1_good=(np.std(normal_tem1))*3
        print("for lab1, if removed the abnormal temperature(1 standard deviation away mean), the possible of temperature is from {low} to {high}\n".format(low=round(np.mean(normal_tem1)-std3_lab1_good,4),high=round(np.mean(normal_tem1)+std3_lab1_good,4)))
    
    if normal_tem2:
        std3_lab1_good=(np.std(normal_tem1))*3
        print("for lab1, if removed the the abnormal temperature(2 standard deviation away mean), the possible of temperature is from {low} to {high}\n".format(low=round(np.mean(normal_tem1)-std3_lab1_good,4),high=round(np.mean(normal_tem1)+std3_lab1_good,4)))
    
    if normal_tem3:
        std3_lab1_good=(np.std(normal_tem1))*3
        print("for lab1, if removed the the abnormal temperature(3 standard deviation away mean), the possible of temperature is from {low} to {high}\n".format(low=round(np.mean(normal_tem1)-std3_lab1_good,4),high=round(np.mean(normal_tem1)+std3_lab1_good,4)))
    