#prepare data

import csv
import smbus
import time
import serial
import sklearn
import numpy as np
import pandas as pd
from time import sleep
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
#arduino = serial.Serial('com18',115200)

bus = smbus.SMBus(1)
SLAVE_ADDRESS = 0x08
i2c_array = []

def requestreading():
    block = bus.read_i2c_block_data((SLAVE_ADDRESS), 0, 11)

    for i in block:
        variable = valmap(i, 0.0, 255.0, 0.0, 5000.0)
        i2c_array.append(variable)
        
    return i2c_array

def valmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def sharp_prediction(thumb_sup=[],thumb_inf=[],index=[]):
    
    data_frame = pd.DataFrame({'sensor1': thumb_sup,'sensor2': thumb_inf,'sensor3': index})
    data_frame.replace(' ', 0)
    #transform to int and replace non numeric value to NaN
    #data_frame = data_frame.apply(pd.to_numeric, errors='coerce')
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
        
    dt = pd.DataFrame({'maximum s1': maxi_sens1,'maximum s2': maxi_sens2, 'diff_mean': moy,'mean_s1': moy_sens1, 'mean_s2': moy_sens2, 'mean_s3': moy_s3}, columns = ['maximum s1', 'maximum s2', 'diff_mean', 'mean_s1', 'mean_s2', 'mean_s3'], index=[0])
    data_test = dt.iloc[ 0 , : ]
    data_test = data_test.values
    
    # Load the model from the file 
    knn_from_joblib = joblib.load('sharpness_model.pkl')  
    # Use the loaded model to make predictions 
    predicted = knn_from_joblib.predict([data_test]) 
    
    return predicted
    
def stiff_prediction(thumb=[],index=[],middle=[],ring=[],pinky=[]): 
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
    

        
    dt = pd.DataFrame({'mean_s1':  moy_sens1, 'mean_s2': moy_sens2, 'mean_s3': moy_sens3, 'mean_s4': moy_sens4, 'mean_s5': moy_sens5, 'diff_mean1': moy_s1_s2, 'diff_mean2': moy_s1_s2s3}, columns = ['mean_s1', 'mean_s2', 'mean_s3', 'mean_s4', 'mean_s5', 'diff_mean1', 'diff_mean2'], index=[0])
    data_test = dt.iloc[ 0 , : ]
    data_test = data_test.values 
    
    # Load the model from the file 
    knn_from_joblib = joblib.load('stiffness_model.pkl')  
    # Use the loaded model to make predictions 
    predicted = knn_from_joblib.predict([data_test])
 
    return predicted
    
thumb_sup = []
thumb_inf = []
index = []
middle = []
ring = []
pinky = []


#input configuration
print ('please put your sensor in contact with object and dont interrupt')
#sample_number = input ("Are you ready ! ! ")
time.sleep(3)
sample = 150

start = time.clock()
millis = 0  
cnt = 0 

while 1:
    try: 
        arduinoarray = requestreading()
        thumb_sup.append(arduinoarray[0])
        thumb_inf.append(arduinoarray[1])
        index.append(arduinoarray[2])
        middle.append(arduinoarray[3])
        ring.append(arduinoarray[4])
        pinky.append(arduinoarray[5])
        #print (cnt)
    except:
        start = time.clock()
        
        del thumb_sup[0 : sample+1] 
        del thumb_inf[0 : sample+1] 
        del index[0 : sample+1]
        del middle[0 : sample+1] 
        del ring[0 : sample+1] 
        del pinky[0 : sample+1]

    if(len(thumb_sup) == sample):
        del thumb_sup[113 : sample+1]
        del thumb_inf[113 : sample+1]
        del index[113 : sample+1]
        del middle[113 : sample+1]
        del ring[113 : sample+1]
        del pinky[113 : sample+1]
       
        #print len(thumb_sup)
        
        #prediction 
        val_sharp = sharp_prediction(thumb_sup,thumb_inf,index)
        val_stiff = stiff_prediction(thumb_sup,index,middle,ring,pinky)
        if val_sharp[0]== 1 and val_stiff[0]== 1:
            bus.write_byte(0x08, 1)
            
        if val_sharp[0]== 0 and val_stiff[0]== 1:
            bus.write_byte(0x08, 0)
            print ("sharp object")
        if val_sharp[0]== 0 and val_stiff[0]== 0:
            bus.write_byte(0x08, 0)
            print ("sharp object")
        if val_sharp[0]== 0 and val_stiff[0]== 2:
            bus.write_byte(0x08, 0)
            print ("sharp object")
            
        if val_sharp[0]== 2 and val_stiff[0]== 1:
            bus.write_byte(0x08, 2)  
            print ("flat object")
            
        if val_sharp[0]== 1 and val_stiff[0]== 0:
            bus.write_byte(0x08, 3)
            print ("hard object")
        if val_sharp[0]== 2 and val_stiff[0]== 0:
            bus.write_byte(0x08, 3)
            print ("hard object")           
        if val_sharp[0]== 2 and val_stiff[0]== 2:
            bus.write_byte(0x08, 4)  
            print ("soft object")
            

        cnt = cnt +1 
        del thumb_sup[0 : sample+1] 
        del thumb_inf[0 : sample+1] 
        del index[0 : sample+1]
        del middle[0 : sample+1] 
        del ring[0 : sample+1] 
        del pinky[0 : sample+1]
        
        millis = time.clock()-start
        #print cnt

