import os,sys
import psse35
import psspy
import dyntools

ConvCaseName = sys.argv[1]
SnapName = sys.argv[2]
ContFileName = "No_Fault.idv"
ContName = ContFileName.replace('.idv','')
LogFileName = SnapName.replace('.snp','') + "_" + ContName + '.log'
CHFName = SnapName.replace('.snp','') + "_" + ContName + '.out'

if __name__ == "__main__":
    #set current working directory
    file_dir = os.path.dirname(__file__)
    os.chdir(file_dir)
    LogFilePath = os.path.join(file_dir, LogFileName)
    psspy.psseinit(200000)
            
    #direct dynamics output to log
    psspy.progress_output(2,LogFilePath,[0,0])
    psspy.prompt_output(4,r"""4""",[0,0])
    psspy.report_output(4,r"""4""",[0,0])
    psspy.alert_output(4,r"""4""",[0,0])
            
    #load cases, set simulation options
    CNVDirFileName = LogFilePath = os.path.join(file_dir, ConvCaseName)
    psspy.case(CNVDirFileName)
    SnapDirFileName = os.path.join(file_dir, SnapName)
    psspy.rstr(SnapDirFileName)
    psspy.case_title_data(ConvCaseName,ContName)
    psspy.set_zsorce_reconcile_flag(1)
    psspy.set_model_debug_output_flag(0)
    psspy.set_relang(1,3011,r"""1""") #generator at system swing
    ierr = psspy.set_load_model_thresh( lmwthresh   = 5.0, lpqthresh   = 1.4327, lvtthresh   = 0.93) #load modeling thresholds
    
    #Set channels for plotting
    psspy.delete_all_plot_channels()
    ierr = psspy.bsys(sid=0,usekv=1,basekv=[100.,999.],numarea=1,areas=[1])
    psspy.chsb(0,0,[-1,-1,-1,1,12,0]) #bus frequency for buses at least 100 kV
    psspy.chsb(0,0,[-1,-1,-1,1,13,0]) #bus voltage for buses at least 100 kV
    ierr = psspy.asys(sid=0, num=1, areas=[1])
    psspy.chsb(0,0,[-1,-1,-1,4,25,0]) #include PLOAD Area 1 (as well as other Area 1 P totals)

    #initialize and run to one second
    print("\nInitializing:  " + ConvCaseName + " " + ContName + "\n")
    CHFDirFileName = os.path.join(file_dir, CHFName)
    psspy.strt_2([0,1],CHFDirFileName)
    psspy.run(0,1.0,240,21,0)

    #Run Contingency
    print("\nApplying Contingency: " + ContName + "\n")
    ContDirFileName = os.path.join(file_dir, ContFileName)
    psspy.runrspnsfile(ContDirFileName)
    
    #run to simulation end time (60 seconds for now)
    print("\nRunning to 60 seconds...\n")
    psspy.run(1,60.0,240,21,0)  #show convergence monitor, but keep other log printing limited to about once per second
    
    #redirect output back to GUI
    psspy.progress_output(1,LogFilePath,[0,0])
    ierr = psspy.pssehalt_2()     

    print("\nProgram Complete")