#prepare data

import csv
import time
import serial
import sklearn
import numpy as np
import pandas as pd
from time import sleep
arduino = serial.Serial('com18',115200)


def make_dataset(obj,thumb=[],index=[],middle=[],ring=[],pinky=[]): 
    data_frame = pd.DataFrame({'sensor1': thumb,'sensor2': index,'sensor3': middle,'sensor4': ring,'sensor5': pinky})
        
    data_frame.replace(' ', 0)
    #transform to int and replace non numeric value to NaN
    data_frame = data_frame.apply(pd.to_numeric, errors='coerce')
    #replace NaN value with zero
    data_frame = data_frame.fillna(0)
    
    #Stiffness
    data_frame['diff'] = data_frame['sensor1'].sub(data_frame['sensor2'], axis = 0)
    data_frame['sum'] = data_frame['sensor2'] + data_frame['sensor3']
    data_frame['diff_3fing'] = data_frame['sensor1'].sub(data_frame['sum'], axis = 0)
    
    moy_sens1= data_frame.loc[:,"sensor1"].mean()
    moy_sens2= data_frame.loc[:,"sensor2"].mean()
    moy_sens3 = data_frame.loc[:,"sensor3"].mean()
    moy_sens4 = data_frame.loc[:,"sensor4"].mean()
    moy_sens5 = data_frame.loc[:,"sensor5"].mean()
    moy_s1_s2 = data_frame.loc[:,"diff"].mean()
    moy_s1_s2s3 = data_frame.loc[:,"diff_3fing"].mean()
    

        
    dt = pd.DataFrame({'mean_s1':  moy_sens1, 'mean_s2': moy_sens2, 'mean_s3': moy_sens3, 'mean_s4': moy_sens4, 'mean_s5': moy_sens5, 'diff_mean1': moy_s1_s2, 'diff_mean2': moy_s1_s2s3, 'label':[obj]}, columns = ['mean_s1', 'mean_s2', 'mean_s3', 'mean_s4', 'mean_s5', 'diff_mean1', 'diff_mean2', 'label'])
        
    with open('stiffness_data.csv', 'a') as f:
        dt.to_csv(f, header = False, index = False)
        #f.write("\n")
        
        
    
thumb_sup = []
thumb_inf = []
index = []
middle = []
ring = []
pinky = []





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
            middle.append(arduinoarray[3])
            ring.append(arduinoarray[4])
            pinky.append(arduinoarray[5])
    except:
        start = time.clock()

    if(len(pinky) == sample):
        
        del thumb_sup[113 : sample+1]
        del thumb_inf[113 : sample+1]
        del index[113 : sample+1]
        del middle[113 : sample+1]
        del ring[113 : sample+1]
        del pinky[113 : sample+1]
        #print len(thumb_sup)
        make_dataset(obj_class,thumb_sup,index,middle,ring,pinky)
        
        cnt = cnt +1 
        
        del thumb_sup[0 : sample+1] 
        del thumb_inf[0 : sample+1] 
        del index[0 : sample+1]
        del middle[0 : sample+1] 
        del ring[0 : sample+1] 
        del pinky[0 : sample+1]
        
        millis = time.clock()-start
        print millis
        #print cnt


    
