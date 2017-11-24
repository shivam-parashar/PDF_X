import convert
import universal
import commands
import excelwriter
import Parser
import logwriter
import mysql 
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import shutil

def burstpdf():
  file = open("copy"+universal.filename, 'rb')
  infile = PdfFileReader(file)
  no_of_pages = infile.getNumPages()
  for i in range(infile.getNumPages()):
      p = infile.getPage(i)
      outfile = PdfFileWriter()
      outfile.addPage(p)
      with open(universal.pdf_folder+'/%d.pdf' % i, 'wb') as f:
          outfile.write(f)
  file.close()
  return no_of_pages
##def run_command(string,flag=0):
##  if commands.getstatusoutput(string)[0]==1:
##     raise NameError("ERROR IN Commands.getstatusoutput "+string)
##  if flag==1:   
##    return commands.getstatusoutput(string)[1]   
def initial():
  #run_command("mkdir "+universal.pdf_folder)
  os.mkdir(universal.pdf_folder)
  #run_command("mkdir "+universal.tag_folder)
  os.mkdir(universal.tag_folder)
  temp=universal.filename #assigning filename to temp
  no_of_pages=burstpdf()
  logwriter.logwrite("\n********"+"\n"+temp+"\n*************\n")  
  if no_of_pages==0:
    logwriter.logwrite("No pages in this pdf\n")
    logwriter.logwrite("********"+"\n"+temp+"\n*************\n")
    return 0
  i=0  
  excelwriter.init()
  while i<no_of_pages:    #loop for locating first patent file
    universal.filename=str(i);
    convert.convert() #for initializing conversion of files
    i+=1
    if(Parser.begin()!=-1):
      excelwriter.loop()
      mysql.loop()
      break 
  universal.flag=1 #Process of extraction will start    
  #print (universal.con)
  while i<no_of_pages:
   universal.filename=str(i)
   convert.convert() #for initializing conversion of files
   if(Parser.begin()==-1):
    i+=1
    continue 
   excelwriter.loop() 
   mysql.loop()
   i+=1
  universal.workbook.close()  
  #run_command("rm -r "+universal.pdf_folder)
  shutil.rmtree(universal.pdf_folder)
  #run_command("rm -r "+universal.tag_folder)
  shutil.rmtree(universal.tag_folder)
  logwriter.logwrite("********"+"\n"+temp+"\n*************\n")
