#filename is set to universal.logfile.txt
import universal
def logwrite(log):
    log_file = open(universal.logfile+".txt","a")
    log_file.write(str(log)+str('\n'))
    log_file.close()
