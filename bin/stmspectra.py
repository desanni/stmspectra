import argparse
import matplotlib.pyplot as plt
import spectra_analysis
import parameters
import plot_spectra

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "STM Spectra Plotting Tool. By defaults, this program plots the conductance of the .VERT files you supply in the command line.")
    parser.add_argument("files", help=".VERT file(s) for the spectra you want to plot", nargs = '+')
    parser.add_argument("-l", "--labels", nargs = '+',help="Can choose to input labels for each spectra, if you use this argument, make sure you have the same number of files and labels")
    parser.add_argument("-v", "--verbose", action="store_true", help="print out details for each .VERT file")
    parser.add_argument("-r", "--ramp", action="store_true", help="show voltage and z ramp for each .VERT file")
    parser.add_argument("-I", "--current", action="store_true", help="plot current instead of conductance")
    parser.add_argument("-a", "--average", action="store_true", help="average spectra (either current or conductance) before plotting")
    parser.add_argument("--hyst", action="store_false", help="turn off hystersis correction, default is to do the correction")
    parser.add_argument("-n", "--normalize", action="store_true", help="normalize the spectra by multiplying by exp(-2*kappa*z), you can set the value of kappa with --k")
    parser.add_argument("-k", "--kappa", default=1.0, type=float, help="value of kappa [Ang^-1] in normalization, default value is 1.0 Ang^-1, [type=float]")
    parser.add_argument("-A", "--Average", action="store_true", help="Average all the input spectra together, input numbers for something")
    parser.add_argument("-s", "--split", default = 0, type=int, nargs='+', help="This flag can be used to split the input file list into sets of spectra that you want to average together. You can input as many integers here as necessary, each interger corresponds to the ith spectra starting a new set of averaged spectra")
    parser.add_argument("-av", "--abs_value", action="store_false", help="by default, stmspectra -I plots the absolute value of the current, use this fl to turn it off and plot the real value (log scale will automatically turn off)")
    parser.add_argument("-fs", "--fontsize", default=20.0, type=float, help="fontsize for plots, [type=float]")
    parser.add_argument("--figsize", type=float, nargs = 2, help="figure size for plots, [type=tuples]")
    parser.add_argument("-lw", "--linewidth", default=2.0, type=float, help="linewidth for plots, [type=float]")
    parser.add_argument("-log", "--logscale", action="store_false", help="Use this flag to turn off the log scale for the current and conductance plots")
    parser.add_argument("-g", "--grid", action="store_false", help="Use this flag to turn off the grid, by default the grid appears on all plots")
    parser.add_argument("--xlim", type=float, nargs = 2, help="x limits for plot, in Volts, [type=tuple]")
    parser.add_argument("--ylim", type=float, nargs = 2, help="y limits for plot, in Amps, [type=tuple]")
    parser.add_argument("--legend", action="store_false", help="Use this flag to not display a legend, default is to show one")
    parser.add_argument("--xlabel", type=str, nargs = '+',help="Use this to set the label on the x-axis, [type=str]")
    parser.add_argument("--ylabel", type=str, nargs = '+', help="Use this to set the label on the y-axis, [type=str]")
    parser.add_argument("--savefig", type=str, help="use this command to save the resulting figure, input desired filename including extension, [type=str]")

    args = parser.parse_args()

    print ' '
    for f, i in zip(args.files, range(len(args.files))):
        print 'file: ' + f
        if args.verbose:
            print spectra_analysis.spectra(f), '\n'

    #If all arguments = False, then plot the conductance

    if args.ramp is False and args.current is False and args.Average is False:

        if args.figsize is None:
            figsize = (10,8)
        else:
            figsize = (args.figsize[0], args.figsize[1])

        if args.xlabel is None:
            xlabel = None
        else:
            xlabel = ''
            for text in args.xlabel:
                xlabel += text

        if args.ylabel is None:
            ylabel = None
        else:
            ylabel = ''
            for text in args.xlabel:
                ylabel += text

        plt.figure(figsize = figsize)
        plot_spectra.conductance_plot(args.files, labels = args.labels, average = args.average, hyst = args.hyst, normalize = args.normalize, kappa = args.kappa, fontsize = args.fontsize, linewidth = args.linewidth, logscale = args.logscale, grid = args.grid, xlim = args.xlim, ylim = args.ylim, legend = args.legend, xlabel = xlabel, ylabel = ylabel)

    elif args.current is True and args.Average is False:

        
        if args.figsize is None:
            figsize = (10,8)
        else:
            figsize = (args.figsize[0], args.figsize[1])

        if args.xlabel is None:
            xlabel = None
        else:
            xlabel = ''
            for text in args.xlabel:
                xlabel += text

        if args.ylabel is None:
            ylabel = None
        else:
            ylabel = ''
            for text in args.xlabel:
                ylabel += text

        plt.figure(figsize = figsize)
        plot_spectra.current_plot(args.files, labels = args.labels, abs_value = args.abs_value, average = args.average, hyst = args.hyst, normalize = args.normalize, kappa = args.kappa, fontsize = args.fontsize, linewidth = args.linewidth, logscale = args.logscale, grid = args.grid, xlim = args.xlim, ylim = args.ylim, legend = args.legend, xlabel = xlabel, ylabel = ylabel)

    elif args.ramp is True:
        
        if args.figsize is None:
            figsize = (8, 4 * len(args.files))
        else:
            figsize = (args.figsize[0], args.figsize[1])

        plot_spectra.show_ramp(args.files, labels = args.labels, figsize = figsize,fontsize = args.fontsize, linewidth = args.linewidth, grid = args.grid)

    elif args.Average is True:

        if args.split == 0:
            file_list = [args.files]
        else:
            file_list = []
            for i in range(len(args.split)+1):
                if i == 0:
                    file_list.append(args.files[0:args.split[i]-1])
                elif i == len(args.split):
                    file_list.append(args.files[args.split[i-1]-1:len(args.files)])
                else:
                    file_list.append(args.files[args.split[i-1]:args.split[i]])
                                    
        if args.figsize is None:
            figsize = (10,8)
        else:
            figsize = (args.figsize[0], args.figsize[1])

        if args.xlabel is None:
            xlabel = None
        else:
            xlabel = ''
            for text in args.xlabel:
                xlabel += text

        if args.ylabel is None:
            ylabel = None
        else:
            ylabel = ''
            for text in args.xlabel:
                ylabel += text

        plt.figure(figsize = figsize)
        if args.current is False:
            plot_spectra.average_conductance_plot(file_list, labels = args.labels, average = True, hyst = args.hyst, normalize = args.normalize, kappa = args.kappa, fontsize = args.fontsize, linewidth = args.linewidth, logscale = args.logscale, grid = args.grid, xlim = args.xlim, ylim = args.ylim, legend = args.legend, xlabel = xlabel, ylabel = ylabel)
        elif args.current is True:
            plot_spectra.average_current_plot(file_list, labels = args.labels, abs_value = args.abs_value, average = True, hyst = args.hyst, normalize = args.normalize, kappa = args.kappa, fontsize = args.fontsize, linewidth = args.linewidth, logscale = args.logscale, grid = args.grid, xlim = args.xlim, ylim = args.ylim, legend = args.legend, xlabel = xlabel, ylabel = ylabel)


    plt.tight_layout()

    if args.savefig is not None:
        plt.savefig(args.savefig)
#show figures at the end
    plt.show()        
