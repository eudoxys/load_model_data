#Needs to have matplotlib and numpy installed for dyntools:  py -m pip install matplotlib

import os,sys
import psse35
import dyntools


CHFFileName = sys.argv[1]
PlotFileName = CHFFileName.replace('.out','.pdf')

def ScanChans(outfile = '', plotPdfFile = ''):
    print("\nProcessing " + outfile + "\n")
    
    Results = []
    
    chnfobj = dyntools.CHNF(outfile, outvrsn=1)
    short_title, chanid, chandata = chnfobj.get_data()  #this will get all channels and the time channel
    
    #These lists will be used to create a set of plots 
    VoltIDs = []
    FreqIDs = []
    PLODIDs = []
    
    for EachId in chanid.items():
        if (EachId[1][0:4]) == 'FREQ':
            FreqIDs.append(EachId[0])
        elif (EachId[1][0:4]) == 'VOLT':
            VoltIDs.append(EachId[0])
        elif (EachId[1][0:5]) == 'PLOAD':  
            PLODIDs.append(EachId[0])
        else:
            pass
       
    #Create Plot files
    print("\n Creating Plot Files\n")
    ChanTimes = chandata['time']
    EndTimeIdx = len(ChanTimes)-1
    StartTimeIdx = 0
    chanrange = chnfobj.get_range()  #this will place the range of all the channel files into a dictionary
    optnfmt  = {'rows':2,'columns':2,'dpi':300,'showttl':True, 'showoutfnam':False, 'showlogo':False,
        'legendtype':1, 'addmarker':False}
    XscaleMax = chandata['time'][EndTimeIdx]
    optnchn = {} #dictionary to hold polot output selection
    PlotBlockNum = 0

    #Study area Load (P)
    ymin = chanrange[PLODIDs[0]]['min'] - 20.0
    ymax = chanrange[PLODIDs[0]]['max'] + 20.0
    PlotBlockNum = PlotBlockNum + 1
    PlotBlockDict = {'chns': [PLODIDs[0]], 
          'title': 'Study Area Total Real Load',
          'ylabel': 'Power (MW)', 
          'xlabel': 'Time (Seconds)',
          'xscale': [0.0,XscaleMax], 
          'yscale': [ymin,ymax]}
    #add new block with the current block number to the output dictionary
    optnchn[PlotBlockNum] = PlotBlockDict  

    
    #Study Area Bus Frequencies
    Count = 0
    plotchans = []
    for FreqIdx in FreqIDs:
        #placing up to six voltage plots on the same block
        plotchans.append(FreqIDs[Count])
        plotchans.append('v*60.0+60.0')
        Count = Count + 1
        if (Count % 6 == 0) or (Count == len(FreqIDs)):
            PlotBlockNum = PlotBlockNum + 1
            ymin = 57.0
            ymax = 62.0
            PlotBlockDict = {'chns': plotchans, 
              'title': 'Bus Frequencies',
              'ylabel': 'Frequency (Hz)', 
              'xlabel': 'Time (Seconds)',
              'xscale': [0.0,XscaleMax], 
              'yscale': [ymin,ymax]}
            #add new block with the current block number to the output dictionary
            optnchn[PlotBlockNum] = PlotBlockDict
            plotchans = []
    
    #Study Area Bus Voltages
    Count = 0
    plotchans = []
    for VoltIdx in VoltIDs:
        #placing up to six voltage plots on the same block
        plotchans.append(VoltIDs[Count])
        Count = Count + 1
        if (Count % 6 == 0) or (Count == len(VoltIDs)):
            PlotBlockNum = PlotBlockNum + 1
            ymin = 0.0
            ymax = 1.50
            PlotBlockDict = {'chns': plotchans, 
              'title': 'PU Voltages',
              'ylabel': 'Voltage (P.U.)', 
              'xlabel': 'Time (Seconds)',
              'xscale': [0.0,XscaleMax], 
              'yscale': [ymin,ymax]}
            #add new block with the current block number to the output dictionary
            optnchn[PlotBlockNum] = PlotBlockDict
            plotchans = []

        
    
    #send the plot dictionaries to create the PDFs
    retvfiles = chnfobj.xyplots(optnchn,optnfmt,plotPdfFile)
    print(' Plots created in ' + plotPdfFile + '\n')
    chnfobj.plots_close()
    
    return None
    
if __name__ == "__main__":
    #set current working directory 
    file_dir = os.path.dirname(__file__)
    os.chdir(file_dir)
    
    CHFDirFileName = os.path.join(file_dir, CHFFileName)
    PlotDirFileName = os.path.join(file_dir, PlotFileName)
            
    ScanChans(CHFDirFileName, PlotDirFileName)
                
    
    print("\nProgram Complete\n")
