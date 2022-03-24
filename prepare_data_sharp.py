#prepare data

import csv
import time
import serial
import sklearn
import numpy as np
import pandas as pd
from time import sleep
arduino = serial.Serial('com18',115200)


def make_dataset(obj,thumb_sup=[],thumb_inf=[],index=[]):
    
    
    data_frame = pd.DataFrame({'sensor1': thumb_sup,'sensor2': thumb_inf,'sensor3': index})
    data_frame.replace(' ', 0)
    #transform to int and replace non numeric value to NaN
    data_frame = data_frame.apply(pd.to_numeric, errors='coerce')
    #replace NaN value with zero
    data_frame = data_frame.fillna(0)
    #sharpness
    data_frame['diff'] = data_frame['sensor1'].sub(data_frame['sensor2'], axis = 0)
    moy_sens1= data_frame.loc[:,"sensor1"].mean()
    moy_sens2= data_frame.loc[:,"sensor2"].mean()
    moy = data_frame.loc[:,"diff"].mean()
    maxi_sens1= data_frame['sensor1'].max()
    maxi_sens2 = data_frame['sensor2'].max()
    moy_s3 = data_frame.loc[:,"sensor3"].mean()
        
    #dt = pd.DataFrame({'maximum s1': maxi_sens1,'maximum s2': maxi_sens2, 'means': moy,'STD_s1': std_sens1, 'STD_s2': std_sens2}, index=[0])
    dt = pd.DataFrame({'maximum s1': maxi_sens1,'maximum s2': maxi_sens2, 'diff_mean': moy,'mean_s1': moy_sens1, 'mean_s2': moy_sens2, 'mean_s3': moy_s3, 'label':[obj]}, columns = ['maximum s1', 'maximum s2', 'diff_mean', 'mean_s1', 'mean_s2', 'mean_s3', 'label'])
        
    with open('sharpness_data.csv', 'a') as f:
        dt.to_csv(f, header = False, index = False)
        #f.write("\n")
    
thumb_sup = []
thumb_inf = []
index = []





#input configuration
print 'please put your sensor in contact with object and dont interrupt'
object_incontact = input ("what's ur object nature: ")
obj_class = int(object_incontact)

window_time_str = input ("Enter the segment number: ")
window_time = int(window_time_str)
sample_number = input ("Enter sample number: ")
sample = int(sample_number)
time.sleep(5)
start = time.clock()
millis = 0  
cnt = 0 

while cnt < window_time:
    try: 
        
        if(arduino.inWaiting()>0): 
            response = arduino.readline()
            arduinoarray = response.split(',')
            thumb_sup.append(arduinoarray[0])
            thumb_inf.append(arduinoarray[1])
            index.append(arduinoarray[2])
    except:
        start = time.clock()

    if(len(thumb_sup) == sample):
        del thumb_sup[113 : sample+1]
        del thumb_inf[113 : sample+1]
        del index[113 : sample+1]
        #print len(thumb_sup)
        make_dataset(obj_class,thumb_sup,thumb_inf,index)
        
        cnt = cnt +1 
        
        del thumb_sup[0 : sample+1] 
        del thumb_inf[0 : sample+1] 
        del index[0 : sample+1]
        
        millis = time.clock()-start
        print millis
        #print cnt


    
