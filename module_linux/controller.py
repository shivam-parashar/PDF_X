import main
import universal
import browser
import mysql
from shutil import copyfile
universal.init()
mysql.init()
files=browser.browse()
for _file in files :
  #main.run_command("cp "+str(_file)+" "+universal.current_dir)
  src=str(_file)
  universal.filename=""
  temp=len(_file)-1
  while _file[temp]!="/":
    universal.filename=_file[temp]+universal.filename
    temp-=1
  dst=str(universal.current_dir+'/'+str(universal.filename))
  copyfile(src,dst)
  universal.logfile=universal.filename #as univeral.filename changes in main   
  mysql.createconnection()
  main.initial()
  mysql.closeconnection()
  main.run_command("rm "+universal.logfile)   
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
