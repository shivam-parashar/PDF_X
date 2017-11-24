import main
import universal
import browser
import sqlitewriter
from shutil import copyfile
import os
#import test
universal.init()
sqlitewriter.init()
files=browser.browse()
for _file in files :
  #main.run_command("cp "+str(_file)+" "+universal.current_dir)
  src=str(_file)
  universal.filename=""
  temp=len(_file)-1
  while _file[temp]!="/":
    universal.filename=_file[temp]+universal.filename
    temp-=1
  tempfile = "copy"+universal.filename
  dst=str(universal.current_dir+'/'+str("copy"+universal.filename))
  copyfile(src,dst)
  universal.logfile = universal.filename.replace('.pdf','') #as univeral.filename changes in main   
  sqlitewriter.createconnection()
  main.initial()
  sqlitewriter.closeconnection()
  
  if(universal.logflag==0):
    os.remove(universal.logfile+".txt")
#  else:
#   test.init(tempfile)
  os.remove(tempfile)
  os.remove(_file)
  #main.run_command("rm "+universal.logfile)
#year=input("year\n")
#s=main.run_command("ls "+str(year),1).split("\n")
#fappend.close() 
#for x in s:
#  universal.filename=x
#  main.run_command("mv "+str(year)+"/"+str(x)+" "+universal.current_dir)
#  main.initial()
#  main.run_command("mv "+universal.current_dir+"/"+str(x)+" "+str(year))

#fappend=open("log.txt",'a')   
#fappend.write("\n********"+"\n"+str(year)+"\n*************\n\n\n")
#fappend.close()   
#i=input("Filename\n")
