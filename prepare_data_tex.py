#prepare data

import csv
import time
import serial
import sklearn
import numpy as np
import pandas as pd
from time import sleep
arduino = serial.Serial('com18',115200)

def rms(input_data1):
    rms = np.sqrt(np.mean(np.power(input_data1,2)))
    return rms
def var(data):
    var = np.var(data)
    return var
def ssi(data):
    ssi = np.sum(np.abs(np.power(data,2)))
    return ssi

def wl(data):
    wl = np.sum(np.abs(np.diff(data)))
    return wl


#fft_variables
Fs = 1000.0;  # sampling rate
Ts = 1.0/Fs; # sampling interval
t = np.arange(0,1,Ts) # time vector

def fft_transform(thumb_sup=[]):
    data_frame = pd.DataFrame({'signal': thumb_sup})
    data_frame.replace(' ', 0)
    #transform to int and replace non numeric value to NaN
    data_frame = data_frame.apply(pd.to_numeric, errors='coerce')
    #replace NaN value with zero
    data_frame = data_frame.fillna(0)
    
    thumb_sup = data_frame["signal"].values

    n = len(thumb_sup)
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range

    Y = np.fft.fft(thumb_sup)/n # fft computing and normalization
    Y = abs(Y[range(n/2)])
    return frq,Y

def make_dataset(obj,index=[]):
    fft_frq,fft_amp = fft_transform(index)
    data_frame = pd.DataFrame({'frequency': fft_frq, 'amplitude': fft_amp})
    data_frame = data_frame.head(10)
    
    data_frame['diff_tex'] = data_frame['frequency'].sub(data_frame['amplitude'], axis = 0)
    #texture_df = texture_df.head(10)     
    std_tex1 = wl(fft_amp)
    std_tex2 = var(fft_amp)
    maxi_tex1 = rms(fft_amp)
    maxi_tex2 = ssi(fft_amp)
    moy_tex = data_frame.loc[:,"diff_tex"].mean()  
    


    dt = pd.DataFrame({'RMS': maxi_tex1,'SSI': maxi_tex2, 'means': moy_tex,'WL': std_tex1, 'VAR': std_tex2, 'label':[obj]}, columns = ['RMS', 'SSI', 'means', 'WL', 'VAR', 'label'])
     
    with open('texture_data.csv', 'a') as f:
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
        make_dataset(obj_class,index)
        
        cnt = cnt +1 
        
        del thumb_sup[0 : sample+1] 
        del thumb_inf[0 : sample+1] 
        del index[0 : sample+1]
        
        millis = time.clock()-start
        print millis
        #print cnt