#This is an example script to set the initial fixed taps of the transformer within the CMLDBLU2 load model near the center of 
#   the voltage target range for the LTC control (even if LTC control is disabled or set to infinite delay)

#define the bus subsystem to set the initial LTC taps:
Areas = [1,2]
kVThresh = 40.0
ierr = psspy.bsys(1, 1, [kVThresh, 999.0], len(Areas), Areas, 0, [], 0, [], 0, [])

#Loop through each load in in the subsystem
LoadBusNums = []
LoadIDs = []
ierr, LoadBusNums = psspy.aloadint(sid = 1, flag = 4, string=['NUMBER'])
ierr, LoadIDs = psspy.aloadchar(sid = 1, flag = 4, string=['ID'])
count = 0
for eachLoadIndex in range(0,len(LoadBusNums[0])):
    ierr, LoadModName = psspy.lmodnam(ibus=LoadBusNums[0][eachLoadIndex], id= LoadIDs[0][eachLoadIndex],string='CHARAC')
    if ierr == 0:  #if it has an attached load characteristic model, check to see if it is a CMLDBLU2 model
        if 'CMLDBLU2' in LoadModName:  #if it is, set the low side tap according the the voltage
            ierr, Vbus = psspy.busdat(LoadBusNums[0][eachLoadIndex],'PU')
            ierr, StartCONindx = psspy.lmodind(ibus=LoadBusNums[0][eachLoadIndex], id= LoadIDs[0][eachLoadIndex],string1='CHARAC', string2='CON')
            ierr, Vmin = psspy.dsrval('CON', StartCONindx+12)
            ierr, Vmax = psspy.dsrval('CON', StartCONindx+13)
            TargetVolt = (Vmax - Vmin) / 2.0 + Vmin
            TargetTap = TargetVolt/Vbus
            ierr = psspy.change_ldmod_con(ibus=LoadBusNums[0][eachLoadIndex], id= LoadIDs[0][eachLoadIndex], name='CMLDBLU2', j=8, rdata=TargetTap)