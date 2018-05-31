import matplotlib.pyplot as plt
import numpy as np
from spectra_analysis import *
import parameters

V_xlabel = '$E-E_F\ (eV)$'
dIdV_ylabel = r'$\left| \frac{dI}{dV} \right|\ (a.u.)$'
absI_ylabel = r'$|I|\ (A)$'
I_ylabel = r'$I\ (A)$'

def conductance_plot(files, labels = None, average = False, hyst = True, normalize = False, kappa = 1.0, fontsize = 20, linewidth = 2, logscale = True, grid = True, xlim = None, ylim = None, legend = True, xlabel = None, ylabel = None):

    for f, i in zip(files, range(len(files))):
        spec = spectra(f) #load spectra

        if average:
            spec.average(hyst_cor = hyst) #average + hyst correction
        if normalize:
            spec.normalize(kappa) #normalize by exp(-2*kappa*z)

        # assign labels
        if labels is not None:
            label = labels[i]
        else:
            label = spec.label

        #plot spectra
        plt.plot(spec.V, spec.dIdV, linewidth = linewidth, label = label)

    #plotting customization

    if xlabel is None:
        xlabel = V_xlabel
    if ylabel is None:
        ylabel = dIdV_ylabel
        
    plt.xlabel(xlabel, fontsize = fontsize)
    plt.ylabel(ylabel, fontsize = fontsize)
    if legend:
        plt.legend(frameon = False, fontsize = fontsize)
    if logscale:
        plt.yscale('log')
    if grid:
        plt.grid(True)
    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])

def average_conductance_plot(file_list, labels = None, average = True, hyst = True, normalize = False, kappa = 1.0, fontsize = 20, linewidth = 2, logscale = True, grid = True, xlim = None, ylim = None, legend = True, xlabel = None, ylabel = None):

    for files, i in zip(file_list, range(len(file_list))):
        for f in files:
            spec = spectra(f) #load spectra

            if average:
                spec.average(hyst_cor = hyst) #average + hyst correction
            if normalize:
                spec.normalize(kappa) #normalize by exp(-2*kappa*z)

            if i == 0:
                V_avg = spec.V
                dIdV_avg = spec.dIdV
            else:
                dIdV_avg += spec.dIdV

        dIdV_avg /= len(files)
        # assign labels
        if labels is not None:
            label = labels[i]
        else:
            label = None

        #plot spectra
        plt.plot(V_avg, dIdV_avg, linewidth = linewidth, label = label)

    #plotting customization

    if xlabel is None:
        xlabel = V_xlabel
    if ylabel is None:
        ylabel = dIdV_ylabel
        
    plt.xlabel(xlabel, fontsize = fontsize)
    plt.ylabel(ylabel, fontsize = fontsize)
    if legend and labels is not None:
        plt.legend(frameon = False, fontsize = fontsize)
    if logscale:
        plt.yscale('log')
    if grid:
        plt.grid(True)
    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])

def current_plot(files, labels = None, abs_value = True, average = False, hyst = True, normalize = False, kappa = 1.0, fontsize = 20, linewidth = 2, logscale = True, grid = True, xlim = None, ylim = None, legend = True, xlabel = None, ylabel = None):
    
    for f, i in zip(files, range(len(files))):
        spec = spectra(f) #load spectra

        if average:
            spec.average(hyst_cor = hyst) #average + hyst correction
        if normalize:
            spec.normalize(kappa) #normalize by exp(-2*kappa*z)

        # assign labels
        if labels is not None:
            label = labels[i]
        else:
            label = spec.label

        #plot spectra
        if abs_value:
            plt.plot(spec.V, abs(spec.I), linewidth = linewidth, label = label)
        else:
            plt.plot(spec.V, spec.I, linewidth = linewidth, label = label)

    #plotting customization

    if xlabel is None:
        xlabel = V_xlabel
    if ylabel is None and abs_value:
        ylabel = absI_ylabel
    elif ylabel is None:
        ylabel = I_ylabel
        
    plt.xlabel(xlabel, fontsize = fontsize)
    plt.ylabel(ylabel, fontsize = fontsize)
    if legend:
        plt.legend(frameon = False, fontsize = fontsize)
    if logscale and abs_value:
        plt.yscale('log')
    if grid:
        plt.grid(True)
    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])

def average_current_plot(file_list, labels = None, abs_value = True, average = True, hyst = True, normalize = False, kappa = 1.0, fontsize = 20, linewidth = 2, logscale = True, grid = True, xlim = None, ylim = None, legend = True, xlabel = None, ylabel = None):

    for files, i in zip(file_list, range(len(file_list))):
        for f in files:
            spec = spectra(f) #load spectra

            if average:
                spec.average(hyst_cor = hyst) #average + hyst correction
            if normalize:
                spec.normalize(kappa) #normalize by exp(-2*kappa*z)

            if i == 0:
                V_avg = spec.V
                I_avg = spec.I
            else:
                I_avg += spec.I

        I_avg /= len(files)
        # assign labels
        if labels is not None:
            label = labels[i]
        else:
            label = None

        #plot spectra
        if abs_value:
            plt.plot(V_avg, abs(I_avg), linewidth = linewidth, label = label)
        else:
            plt.plot(V_avg, I_avg, linewidth = linewidth, label = label)


    #plotting customization

    if xlabel is None:
        xlabel = V_xlabel
    if ylabel is None:
        ylabel = I_ylabel
        
    plt.xlabel(xlabel, fontsize = fontsize)
    plt.ylabel(ylabel, fontsize = fontsize)
    if legend and labels is not None:
        plt.legend(frameon = False, fontsize = fontsize)
    if logscale and abs_value:
        plt.yscale('log')
    if grid:
        plt.grid(True)
    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])
        
def show_ramp(files, labels = None, figsize = (8, 4), fontsize = 20, linewidth = 2, grid = True):

    fig, axes = plt.subplots(len(files), figsize = figsize)
    
    for f, i in zip(files, range(len(files))):
        if len(files) is 1:
            ax = axes
        else:
            ax = axes[i]

        spec = spectra(f)
        V = spec.V
        z = spec.z
        t = spec.t

        if labels is None:
            ax.set_title(spec.label, fontsize = fontsize)
        else:
            ax.set_title(labels[i], fontsize = fontsize)
        
        # voltage plot
    
        Vline, = ax.plot(t, V, color = 'g', linewidth = linewidth, label = '$V$')
        ax.set_ylabel('$V\ (V)$', fontsize = fontsize)

        # plot z on same plot but show different scale on right hand side
        ax2 = ax.twinx()
        zline, = ax2.plot(t, z, color = 'b', linewidth = linewidth, label = '$z$')
        ax2.set_ylabel('$z\ (Ang)$', fontsize = fontsize)
        ax.grid(grid)

    if len(files) is 1:
        axes.set_xlabel('$time\ (s)$', fontsize = fontsize)
        axes.legend(handles = [Vline, zline], frameon = False, fontsize = fontsize)
    else:
        axes[-1].set_xlabel('$time\ (s)$', fontsize = fontsize)
        axes[-1].legend(handles = [Vline, zline], frameon = False, fontsize = fontsize)

