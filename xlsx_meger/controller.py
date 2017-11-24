import universal
import browser
import merger
from shutil import copyfile
import os
#import test
universal.init()
merger.init()
files=browser.browse()
for _file in files :
  #main.run_command("cp "+str(_file)+" "+universal.current_dir)
  src=str(_file)
  universal.filename=""
  temp=len(_file)-1
  while _file[temp]!="/":
    universal.filename=_file[temp]+universal.filename
    temp-=1
  universal.filename = "copy"+universal.filename
  dst=str(universal.current_dir+'/'+str(universal.filename))
  try:
   copyfile(src,dst)
  except e as Exception:
    print(str(e)+" for file "+str(universal.filename))
  merger.readfile()
  os.remove(tempfile)
  os.remove(_file)
universal.workbook.close()  
  
