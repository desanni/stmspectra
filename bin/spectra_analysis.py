import numpy as np
import matplotlib.pyplot as plt
import argparse
import parameters

spec_length_step = parameters.spec_length_step
LockinRC_factor = parameters.LockinRC_factor
skiprows = parameters.skiprows
current_conv = parameters.current_conv

class spectra:
    def __init__(self, filename):
        self.label = filename[-19:-5] #pulls off the filename as the label

        #find all the relevant parameters
        f = open(filename, 'r')
        for line in f:
            if "ZPiezoconst" in line:
                ZPiezoconst = float(line[line.find('=')+1:-1])
            if "LockinRC" in line:
                LockinRC = float(line[line.find('=')+1:-1])*LockinRC_factor #Hz
            if "Vertmandelay" in line:
                Speclength = float(line[line.find('=')+1:-1])*spec_length_step #seconds
            if "VertSpecBack" in line:
                VertSpecBack = int(line[line.find('=')+1:-1])
            if "LockinAmpl" in line:
                LockinAmpl = float(line[line.find('=')+1:-1]) #mV
            if "Current[A]" in line:
                Current = float(line[line.find('=')+1:-1]) #Amps
        f.close()

        #Assign values to spectra object
        self.ZPiezoconst = ZPiezoconst
        self.LockinRC = LockinRC
        self.Speclength = Speclength
        self.VertSpecBack = VertSpecBack
        self.LockinAmpl = LockinAmpl
        self.Current = Current

        #Load spectra data
        data = np.loadtxt(filename, skiprows = skiprows)
        self.data = data #full data if you want it

        #Number of data points, needed for averaging and hysteresis correction 
        N = data.shape[0]
        self.N = N

        #hysteresis correction factor
        hyst = int(N/Speclength/LockinRC/np.pi)
        self.hyst = hyst

        #assign data to spectra values
        self.t = np.linspace(0, self.Speclength, self.N) #time in seconds
        self.V = data[:, 1] / 1000.0 #Volts
        self.z = data[:, 2] * ZPiezoconst/1000.0 #Ang
        self.I = data[:, 3] / current_conv #current in amps
        self.dIdV = data[:,4] / current_conv #conductance

        #this is just a copy now, but if you average or normalize, this maintains the original spectra
        self.V0 = self.V
        self.z0 = self.z
        self.I0 = self.I
        self.dIdV0 = self.dIdV

    #use command print(spectra_object) to print out a few relevant parameters
    def __str__(self):
        ret = 'label: ' + self.label +'\n'
        ret += 'data points: %d\n' %self.N
        ret += 'VertSpecBack: %d\n' %self.VertSpecBack
        ret += 'Current: %.2e A\n' %self.Current
        ret += 'LockinAmpl: %.1f mV' %self.LockinAmpl
        return ret

    def average(self, hyst_cor = True):
    # this function averages the spectra together, and edits the values of sepctra_object.V, .z, .I, and .dIdV
    #not if you want to get the original values after this, just call e.g. epctra_object.I0
        
        n = self.VertSpecBack + 1 #number of passes you did on the spectra
        N = self.N 
        hyst = self.hyst
        self.V = self.data[:N/n, 1] / 1000.0 #Volts
        self.z = self.data[:N/n, 2] * self.ZPiezoconst/1000.0 #Ang
        I = np.zeros(N/n) #temporary storage, will assign the spectra these values after processing
        dIdV = np.zeros(N/n)

        #for each pass, go through and do the calculation, if there is just one pass, just return the original spectra
        if n > 1:
            for i in range(n):
                j = i*N/n
                k = (i+1)*N/n
                V_temp = self.data[j:k, 1]
                I_temp = np.empty(N/n) #temporary storage that will be used to average the values together
                dIdV_temp = np.empty(N/n)
    
                if hyst_cor is True and V_temp[1] > V_temp[0]:
                    #foward pass condition
                    #shift the current and condtuctance values towards negative voltage by factor hyst/2
                    #for values at the end of the array, just copy the last data point to extend the spectra here
                    I_temp[0:N/n-hyst/2] = self.data[j+hyst/2:k, 3]
                    I_temp[N/n-hyst/2:N/n] = self.data[k-1, 3]
                    dIdV_temp[0:N/n-hyst/2] = self.data[j+hyst/2:k,4]
                    dIdV_temp[N/n-hyst/2:N/n] = self.data[k-1, 4]
                elif hyst_cor is True and V_temp[1] < V_temp[0]:
                    #backward pass condition
                    #shift the current and condtuctance values towards positive voltage by factor hyst/2
                    #extend the other side of the spectra
                    I_temp[0:hyst/2] = self.data[j, 3]
                    I_temp[hyst/2:N/n] = self.data[j:k-hyst/2, 3]
                    dIdV_temp[0:hyst/2] = self.data[j,4]
                    dIdV_temp[hyst/2:N/n] = self.data[j:k-hyst/2, 4]
                elif hyst_cor is False:
                    #no hysteresis correction, just average the spectra
                    I_temp = self.data[j:k, 3]
                    dIdV_temp = self.data[j:k, 4]                
                if V_temp[1] < V_temp[0]:
                    #if going from negative to positive, flip the array to do the averageing correctly
                    I_temp = I_temp[::-1]
                    dIdV_temp = dIdV_temp[::-1]

                # add the temp spectra to the previous values
                I += I_temp
                dIdV += dIdV_temp
            # divide by the number of passes at the end to finish averaging
            self.I = I/n/ current_conv
            self.dIdV = dIdV/n / current_conv
        else:
            print 'Only one spectra taken, no averaging possible'

    #normalize the spectra using an input value of kappa in Ang^-1
    def normalize(self, kappa):
        self.I = self.I * np.exp(-2 * kappa * self.z)
        self.dIdV = self.dIdV * np.exp(-2* kappa * self.z)
