#This is an example script to export a DYR of all load characteristic models within a defined sybsystem

#DYR Name
DYRName = "Example2-TfixLS_export.dyr"

#define bus subsystem for which you would like to export:
Areas = psspy.aareaint(-1, 2, 'NUMBER')[1][0]  #Areas = [<list of areas>]
ierr = psspy.bsys(1, 0, [0.0, 0.0], len(Areas), Areas, 0, [], 0, [], 0, [])

#export DYR
psspy.dyda(1,0,[2,10,0],0,DYRName)