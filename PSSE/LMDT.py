# This is an example script to write bus level composite load models
# (CMLDBLU2) from a specified "MasterLoadMapping" tab in an example LMWG
# workbook

# A powerflow case must be loaded in PSSE and filtered by bus subsystem
# (Subsytem 0) for the buses that have desired load CMLDBLU2 output records.
#   *****Use the PSSE bus subsystem selector prior to running this script

# The MasterLoadMapping tab of the LMWG workbook must contain the Bus Number,
# Load ID, Load Composition, and Feeder columns The "PowerFlow" tab is
# optional and information only (same for the LoadTable_PSSEv35,
# BusTable_PSSEv35, DER, Airport Codes, Load Categories tabs)

# Record writing thresholds must be specificied in "LMWG" tab of workbook
# (C14:C17) The LoadComp and Feeder tabs must contain the values in the
# MasterLoadMapping tab The Motors and PwrEl must contain the values in the
# LoadComp tab

import os
import sys
import pandas as pd

def Export_to_DYR(LoadCmp, Feeder, BusNum, LoadID, kVThresh, i):
    #write the bus
    TempStr = str(BusNum)
    fileID.write(TempStr)
    TempStr = "   'USRLOD'  " + str(LoadID) + " 'CMLDBLU2' 12 1 2 133 27 146 48 0 0 " + '\n'
    fileID.write(TempStr)

    tx_flag = 0
    ierr, BuskV = psspy.busdat(BusNum ,'BASE')
    if ierr == 0:
        if BuskV >= kVThresh:
            tx_flag = 1

    TempStr = "   -1  "
    fileID.write(TempStr)
            
    # 'Feeder
    FeederFound = False
    PF_Feeder = Feeder
    ifedr = 2
    FeederSht_fedr = Feeder_Sheet.Cells(ifedr, 1).Value
    while (FeederSht_fedr != ""):
        if FeederSht_fedr == PF_Feeder:
            # feeder is found, set parameters and print
            Bss = Feeder_Sheet.Cells(ifedr, 2).Value
            Rfdr = Feeder_Sheet.Cells(ifedr, 3).Value
            Xfdr = Feeder_Sheet.Cells(ifedr, 4).Value
            Fb = Feeder_Sheet.Cells(ifedr, 5).Value
            TempStr = "   " + str(Bss) + "   " + str(Rfdr) +  "   " + str(Xfdr) + "   " + str(Fb) + "  "
            fileID.write(TempStr)
            if tx_flag == 1 :
                TempStr = "   " + str(Feeder_Sheet.Cells(ifedr, 6)) + "   \n"
            else:
                TempStr = "   0.000   \n"
            fileID.write(TempStr)
            for j in range(7,13):
                TempStr = "   " + str( Feeder_Sheet.Cells(ifedr, j))
                fileID.write(TempStr)
            fileID.write('\n')
            for j in range(13,19):
                TempStr = "   " + str(Feeder_Sheet.Cells(ifedr, j))
                fileID.write(TempStr)
            fileID.write('\n')
            FeederFound = True
            break
        ifedr = ifedr + 1
        FeederSht_fedr = Feeder_Sheet.Cells(ifedr, 1).Value
    if FeederFound == False:
        #print warnings and quit, as no feeder was found
        print("Error Feeder: {} is not found for line {} Bus {}\n ".format(PF_Feeder, i, BusNum))
        print("a. Add a new record in the Feeder tab, or\n")
        print( "b. Change Feeder column record in MasterLoadMapping tab to match existing one in Feeder tab\n")
        print("LMWG DYR Export Terminated" )
        return True

            
    # 'Load Composition
    LoadCompFound = False
    icmp = 2
    CMPSht_cmp = LoadComp_Sheet.Cells(icmp, 1).Value
    while (CMPSht_cmp != ""):
        if CMPSht_cmp == LoadCmp:
            # 'composition is found, set parameters and print
            for j in range(7,12):
                TempStr = "   " + str(LoadComp_Sheet.Cells(icmp, j))
                fileID.write(TempStr)
            fileID.write('\n')
            LoadCompFound = True
            break
        icmp = icmp + 1
        CMPSht_cmp = LoadComp_Sheet.Cells(icmp, 1).Value
    if LoadCompFound == False:
        # 'Print warnings and quit, as no load composition was found
        print("Error Load Composition: " + str(LoadCmp) + " is not found for line " + str(i))
        print("Bus " + str(BusNum) + " " + "\n")
        print("a. Add a new record in the LoadComp tab, or\n")
        print("b. Change Load Comp column record in PowerFLow tab to match existing one in LoadComp tab\n")
        print("LMWG DYR Export Terminated")
        return True
            
    # 'Power Electronics Load
    PwrelFound = False
    LoadComp_Pwr = LoadComp_Sheet.Cells(icmp, 6).Value
    ipwr = 2
    PWRSht_pwr = PwrEl_Sheet.Cells(1, ipwr).Value
    while (PWRSht_pwr != ""):
        if (PWRSht_pwr == LoadComp_Pwr):
            PFel = PwrEl_Sheet.Cells(2, ipwr).Value
            Vd1 = PwrEl_Sheet.Cells(3, ipwr).Value
            Vd2 = PwrEl_Sheet.Cells(4, ipwr).Value
            TempStr = "   " + str(PFel) + "    " + str(Vd1) + "     " + str(Vd2)
            fileID.write(TempStr)
            FrEl = PwrEl_Sheet.Cells(5, ipwr).Value
            PwrelFound = True
            break
        ipwr = ipwr + 1
        PWRSht_pwr = PwrEl_Sheet.Cells(1, ipwr).Value
    if PwrelFound == False:
        # 'Print error and quit, no power electronics load identifier was found
        print("Error Power Electronic Load: " + str(LoadComp_Pwr) + " is not found for line " + str(i))
        print("Bus " + str(BusNum) + "\n")
        print("a. Add a new record in the PwrEl tab, or\n" )
        print("b. Change ID_PwrElec column record in to match existing one in LoadComp tab\n")
        print("LMWG DYR Export Terminated")
        return True
            
    # 'Static Loads
    stat_load = 1
    Pfs = LoadComp_Sheet.Cells(icmp, 12).Value
    P1e = 2
    P2e = 1
    Fr_stat = LoadComp_Sheet.Cells(icmp, 13).Value + LoadComp_Sheet.Cells(icmp, 14).Value
    if (abs(Fr_stat) > 0):
        P1c = LoadComp_Sheet.Cells(icmp, 13).Value / Fr_stat
        P2c = 1 - P1c
    else:
        P1c = 1
        P2c = 1 - P1c
    Pfreq = LoadComp_Sheet.Cells(icmp, 17).Value
    Q1e = 2
    Q2e = 1
    Q1c = LoadComp_Sheet.Cells(icmp, 15).Value
    Q2c = LoadComp_Sheet.Cells(icmp, 16).Value
    Qfreq = LoadComp_Sheet.Cells(icmp, 18).Value
    TempStr = "   " + str(Pfs) + "   " + str(P1e) + "   " + str(P1c) + "   " + str(P2e) + \
        "   " + str(P2c) + "   " + str(Pfreq) + "   \n" + "   " + str(Q1e) + "   " + str(Q1c) + \
        "   " + str(Q2e) + "   " + str(Q2c) + "   " + str(Qfreq) + "\n"
    fileID.write(TempStr)
            
            
    # 'Motor Loads
    MotorType = [0,0,0,0]
    MotorIndex = [-1,-1,-1,-1]
    for imot in range(0, 4):
        LoadCmp_Mtr = LoadComp_Sheet.Cells(icmp, imot + 2).Value
        motor_found = False
        Motor_Sht_Cols = 10 #Number of columns in the motor sheet is hard-coded for now.  Will need future update if columns are added.
        for kmot in  range(2, Motor_Sht_Cols + 1):
            MotorSht_Mot = Motors_Sheet.Cells(1, kmot).Value
            if MotorSht_Mot == LoadCmp_Mtr:
                motor_found = True
                if (Motors_Sheet.Cells(2, kmot).Value == "M3"):
                    MotorType[imot] = 3
                    MotorIndex[imot] = kmot
                elif (Motors_Sheet.Cells(2, kmot).Value == "AC"):
                    MotorType[imot] = 1
                    MotorIndex[imot] = kmot
                else:
                    print("ERROR: Unable to find motor type for Motor " + Motors_Sheet.Cells(1, kmot).Value \
                        + " in Motors table\n" + \
                        + "Solutions: Motor type needs to be M3 or AC\n" + \
                        "LMWG DYR Export Terminated")
                    return True
    if motor_found == False:
        print("ERROR: Motor Load " + LoadCmp_Mtr + " is not found in Motors tab \n" \
                + "Solutions:\n" \
                + " a. Add a new record in Motors tab, or\n" \
                + " b. Change motor load identifier in LoadComp tab for Load Composition to match existing one in Motors tab" \
                + "\nLMWG DYR Export Terminated")
        return True
        
    motor_type = True
    for imot in range(0,3):
        if MotorType[imot] != 3:
            motor_type = False
        if MotorType[3] != 1:
            motor_type = False
        if motor_type == False:
            print("ERROR: Motor Load Composition " + LoadCmp + " has incorrect sequence of motor identifiers\n" \
                + "PSS(R)E requires Motors A, B, and C to be 3-phase and Motor D to be 1-phase\n" \
                + "LMWG DYR Export Terminated")
            return True
    for imot in range(0,4):
        kmot = MotorIndex[imot]
        if MotorType[imot] == 3:
            fileID.write( "   3")
            for j in range(3, 8):
                TempStr = "   " + str(Motors_Sheet.Cells(j, kmot).Value)
                fileID.write(TempStr)
            fileID.write("\n")
            for j in range(8, 12):
                TempStr = "   " + str(Motors_Sheet.Cells(j, kmot).Value)
                fileID.write(TempStr)
            fileID.write("\n")
            for j in range(12, 17):
                TempStr = "   " + str(Motors_Sheet.Cells(j, kmot).Value)
                fileID.write(TempStr)
            fileID.write("\n")
            for j in range(17,22):
                TempStr = "   " + str(Motors_Sheet.Cells(j, kmot).Value)
                fileID.write(TempStr)
            fileID.write("\n")
        else:
            TempStr = "   " + str(Motors_Sheet.Cells(8, kmot).Value) + \
                "   " + str(Motors_Sheet.Cells(11, kmot).Value) + \
                "   " + str(Motors_Sheet.Cells(24, kmot).Value) + \
                "   " + str(Motors_Sheet.Cells(25, kmot).Value) + "\n"
            fileID.write(TempStr)
            for j in range(3, 8):
                TempStr = "   " + str(Motors_Sheet.Cells(j, kmot).Value)
                fileID.write(TempStr)
            fileID.write("\n")
            for j in range(26, 36):
                TempStr = "   " + str(Motors_Sheet.Cells(j, kmot).Value)
                fileID.write(TempStr)
            fileID.write("\n")
            for j in range(9, 11):
                TempStr = "   " + str(Motors_Sheet.Cells(j, kmot).Value)
                fileID.write(TempStr)
            fileID.write("\n")
            for j in range(36, 38):
                TempStr = "   " + str(Motors_Sheet.Cells(j, kmot).Value)
                fileID.write(TempStr)
            fileID.write("\n")
            for j in range(17, 21):
                TempStr = "   " + str(Motors_Sheet.Cells(j, kmot).Value)
                fileID.write(TempStr)
            fileID.write("\n")
            for j in range(21, 24):
                TempStr = "   " + str(Motors_Sheet.Cells(j, kmot).Value)
                fileID.write(TempStr)
            fileID.write("\n")
            for j in range(12, 17):
                TempStr = "   " + str(Motors_Sheet.Cells(j, kmot).Value)
                fileID.write(TempStr)
            fileID.write("\n")
    
    
    # 'write Frcel from Electronics load
    TempStr = "   " + str(FrEl)
    fileID.write(TempStr)
            
            
    # 'Closing comment
    ierr, BusName = psspy.notona(BusNum)
    TempStr = "   /" + BusName +  "   " + "\n"
    fileID.write(TempStr)

    return False

from types import SimpleNamespace

def csv_to_sns(file,
    index_col=[0],
    fillna="",
    ):
    """Read CSV into a SimpleNamespace dict"""

    df = pd.read_csv(file,index_col=index_col).fillna(fillna).to_dict("index")
    return {x:SimpleNamespace(y) for x,y in df.items()}

if __name__ == "__main__":

    #set current working directory and open the excel file to read/write data
    file_dir = os.path.dirname(__file__)
    os.chdir(file_dir)
    
    pd.options.display.width = None
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None

    LMDT = csv_to_sns("LMDT.csv")
    # print(LMDT)

    Map = csv_to_sns("MasterLoadMapping.csv",index_col=[0,1])
    # print(Map)
    
    PowerFlow = csv_to_sns("PowerFlow.csv",index_col=['Type','Bus  Number','Id'])
    # print(PowerFlow)

    LoadComp = csv_to_sns("LoadComp.csv")
    # print(LoadComp)

    Feeder = csv_to_sns("Feeder.csv")
    # print(Feeder)

    Motors = csv_to_sns("Motors.csv")
    # print(Motors)

    MotorsAC = csv_to_sns("MotorsAC.csv")
    # print(MotorsAC)

    PwrEl = csv_to_sns("PwrEl.csv")
    # print(PwrEl)

    DER = csv_to_sns("DER.csv")
    # print(DER)

    dyd_filename=LMDT["DYRfile"].value
    # print(dyd_filename)
    fileID = open(dyd_filename, 'w')
    
    Pmin=LMDT["MinMW"].value
    PQmin=LMDT["PQmin"].value
    Vmin=LMDT["Vmin"].value
    kVThresh=LMDT["kVThresh"].value
    
    quit()

    #Loop through all loads in the subsystem (subsystem 0)
    ierr, [LoadBusNums] = psspy.aloadint(sid = 0, flag = 4, string=['NUMBER'])
    ierr, [LoadIDs] = psspy.aloadchar(sid = 0, flag = 4, string=['ID'])
    ierr, [LoadPQs, DGs] = psspy.aloadcplx(sid=0, flag=4, string=['TOTALACT', 'O_LDGNACT'])
    for eachLoadIndex in range(0,len(LoadBusNums)):
        #check to see that the load meets the defined writing threshold.
        ierr, VoltPU = psspy.busdat(LoadBusNums[eachLoadIndex],'PU')
        LoadMW = LoadPQs[eachLoadIndex].real
        LoadMVAR = LoadPQs[eachLoadIndex].imag
        DERMW = abs(DGs[eachLoadIndex])
        if (LoadMVAR > 0):
            LoadPQ = abs(LoadMW / LoadMVAR)
        else:
            LoadPQ = 999
        if (VoltPU < Vmin) or (LoadPQ < PQmin) or ((LoadMW < Pmin) and (DERMW < Pmin)):
            #Bus writing threshold not met; skip writing this line
            continue
        #check to see that the load is in the mapping tab. If not, print error and skip
        i = 2
        LoadFound = False
        DataError = False
        while(Map_Sheet.Cells(i, 1).Value != "" and DataError == False):
            LoadCmp = Map_Sheet.Cells(i, 3).Value
            Feeder = Map_Sheet.Cells(i, 4).Value
            BusNum = int(str(Map_Sheet.Cells(i, 1).Value).replace('.0',''))
            LoadID = f"{str(Map_Sheet.Cells(i, 2).Value).replace('.0',''):<2}"
            if ((LoadBusNums[eachLoadIndex]==BusNum) and \
                    (LoadIDs[eachLoadIndex]==LoadID) and \
                    (LoadCmp != "") and \
                    (Feeder != "")):
                    #Load is in the spreadsheet and meets the threshold in the workbook, write it to to the DYR
                LoadFound = True
                DataError = Export_to_DYR(LoadCmp, Feeder, BusNum, LoadID, kVThresh, i)
                break
            i += 1
            
        if LoadFound == False:
            print("\nWarning!  Load at Bus '{}' ID: '{}' ".format(LoadBusNums[eachLoadIndex], LoadIDs[eachLoadIndex]))
            print("was not found in the LMWG MasterLoadMapping tab.  Not written to DYR\n")
    
    fileID.close()
    print("\nProgram Complete.  The DYR file is in: " + dyd_filename)

    #close the workbook
    xlBook.Close(True)
    xlApp.Quit()