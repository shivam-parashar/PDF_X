#file containing global variables
import os
def init():
  global tag #records the name of the keys in data dictionary
  tag=["Application No.","Date of filing of Application","Publication Date","Name of Applicant","Title of the invention","Name of Inventor","Abstract","No. of Pages","No. of Claims","International classification","Priority Document No","Priority Date","Name of priority country","International Publication No","International Application No","IAFiling Date","Patent of Addition to Application Number","IBFiling Date","Divisional to Application Number","ICFiling Date"]
  global dbname
  dbname = "patents"
  global tablename
  tablename = "patent_tables" 
  global host
  host = "127.0.0.1"
  global user
  user = "root"
  global password
  password = "123"  
  global data
  data={}
  global tree
  global con
#  global test
#  test=[]
  global datastring
  datastring=""
  global filename #filename of pdf file containing patents
  filename="15"
  global current_dir 
  current_dir=os.getcwd() #In future use in-built python function which is platform independent.
  global pdf_folder  #name of folder containing pdf burst files
  pdf_folder="3"
  global tag_folder #name of folder containing tag-html file
  tag_folder="tag_folder"
  global workbook
  global worksheet
  global date_format
  global row #row counter
  global flag #Flag for process of extraction has started or not 
  flag=0
  global logfile#filename is set to universal.logfile.txt
  logfile=""
  global logflag #for knowing whether something was written to log file or not 
  logflag = 0
