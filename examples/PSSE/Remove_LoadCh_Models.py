# This script can be run from PSSE to remove all load characteristics models from a bus subsytem (prior to adding new CMLD models)
#Note1: this will delete all load characteristic models within the defined bus subsystem, even if those models apply to some
        # buses outside of the defined substyem  (e.g. a CLODZN model for a Zone that is in Area 1 and Area 2 will be deleted
        # even if only Area 1 is defined in the subsystem below)
#Note2: this will only delete Area, Owner, and Zone load characteristic models that have an identifier of '*' in the .dyr file
        #if you have load characteristic models that only apply to certain identifiers, you would need to modify the Lid below
        #(e.g. in your dyr, if you defined CLODAR to apply to Area 1 with load id 'SC' (Small Commercial) then you would need 
        #to modify the Lid on line 37 below to 'SC'.

#define bus subsystem for which you would like to remove loads:
Areas = psspy.aareaint(-1, 2, 'NUMBER')[1][0]  #Areas = [<list of areas>]
ierr = psspy.bsys(1, 0, [0.0, 0.0], len(Areas), Areas, 0, [], 0, [], 0, [])

#Loop through each load in in the subsystem, and if it has an attached load characteristic model, delete that model
LoadBusNums = []
LoadIDs = []
ierr, LoadBusNums = psspy.aloadint(sid = 1, flag = 4, string=['NUMBER','OWNER','ZONE','AREA'])
ierr, LoadIDs = psspy.aloadchar(sid = 1, flag = 4, string=['ID'])
count = 0
for eachLoadIndex in range(0,len(LoadBusNums[0])):
    ierr, LoadModName = psspy.lmodnam(ibus=LoadBusNums[0][eachLoadIndex], id= LoadIDs[0][eachLoadIndex],string='CHARAC')
    if ierr == 0:
        if 'BL' in LoadModName:
            Lodmtype = 0
            Lid = LoadIDs[0][eachLoadIndex]
            Libus = LoadBusNums[0][eachLoadIndex]
        elif 'OW' in LoadModName:
            Lodmtype = 1
            Lid = "*"
            Libus = LoadBusNums[1][eachLoadIndex]
        elif 'ZN' in LoadModName:
            Lodmtype = 2
            Lid = "*"
            Libus = LoadBusNums[2][eachLoadIndex]
        elif 'AR' in LoadModName:
            Lodmtype = 3
            Lid = "*"
            Libus = LoadBusNums[3][eachLoadIndex]
        elif 'AL' in LoadModName:
            Lodmtype = 4
            Lid = "*"
            Libus = LoadBusNums[0][eachLoadIndex] = -1
        ierr = psspy.ldmod_remove(mtype=Lodmtype, ibus=Libus, id=Lid, ltype=1)
        count+= 1


print("\nProgram Complete.  {} load characteristic models removed".format(count))