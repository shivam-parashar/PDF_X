import sqlite3
import universal
import datetime
import logwriter
#init() function creates connection as soon as it starts and ends the same at the end.
#for using loop() function first create a connection using createconnection and after putting all the data close the connection by executing closeconeection
def createconnection():
    try:
        universal.con = sqlite3.connect(universal.dbname+".db")
    except Exception as e:
        logwriter.logwrite(str(e))
        universal.logflag = 1

def closeconnection():
    try:
        universal.con.close()
    except Exception as e:
        logwriter.logwrite(str(e))
        universal.logflag = 1
def transform(tag):
  f = "%d/%m/%Y"
  s=str(universal.data[tag])
  if(s=="NA"):
    s="01/01/0001"
  try:
      ss=datetime.datetime.strptime(s, f)
  except:
      s="01/01/0001"
      ss=datetime.datetime.strptime(s, f)
      logwriter.logwrite("MYSQL: "+tag+"-"+universal.data[tag]+" is not in format on page "+str(int(universal.filename)+1))
  universal.data[tag]=str(ss.year)+"/"+str(ss.month)+"/"+str(ss.day)
 # print(universal.data[tag])
def init():
    try:
        createconnection()
        universal.con.execute("create table if not exists "+universal.tablename+"("+
                  "Application_No varchar(50),"+ 
                  "Date_of_filing_of_Application DATE,"+
                  "Publication_Date DATE,"+
                  "Name_of_Applicant varchar(1000),"+
                  "Title_of_Invention varchar(1000),"+
                  "Name_of_Inventor varchar(1500),"+
                  "Abstract varchar(3500),"+
                  "No_of_Pages INT,"+
                  "No_of_Claims INT,"+
                  "International_Classification varchar(100),"+
                  "Priority_Document_No varchar(70),"+
                  "Priority_date DATE,"+
                  "Name_of_Priority_country varchar(70),"+
                  "International_Publication_No varchar(70),"+
                  "International_Application_No varchar(70),"+
                  "International_Application_No_filing_date DATE,"+
                  "Patent_of_addition_to_Application_No varchar(70),"+
                  "Patent_of_addition_to_Application_No_filing_date DATE,"+
                  "Divisional_Application_No varchar(100),"+
                  "Divisional_Application_No_filing_date DATE"+
                  ")")
        universal.con.commit()
    except Exception as e:
        logwriter.logwrite(str(e))
        universal.logflag = 1
    finally:
        closeconnection()

def loop():
    try:
        transform("Date of filing of Application")
        transform("Publication Date")
        transform("Priority Date")
        transform("IAFiling Date")
        transform("IBFiling Date")
        transform("ICFiling Date")
        if(universal.data["No. of Pages"]=="NA"):
           universal.data["No. of Pages"]='0' 
        if(universal.data["No. of Claims"]=="NA"):
           universal.data["No. of Claims"]='0'
##        if(is_ascii(universal.data["Name of Applicant"])==False):
##            temp = universal.data["Name of Applicant"]
##            universal.data["Name of Applicant"]=unicodedata.normalize('NFKD',temp).encode('ascii','ignore')
##        if(is_ascii(universal.data["Title of the invention"])==False):
##            temp1 = universal.data["Title of the invention"] 
##            universal.data["Title of the invention"]=unicodedata.normalize('NFKD',temp1).encode('ascii','ignore')
##        if(is_ascii(universal.data["Name of Inventor"])==False):
##            temp2 = universal.data["Name of Inventor"]
##            universal.data["Name of Inventor"]=unicodedata.normalize('NFKD',temp2).encode('ascii','ignore')
##        if(is_ascii(universal.data["Abstract"])==False):
##            temp3=universal.data["Abstract"]
##            universal.data["Abstract"]=unicodedata.normalize('NFKD',temp3).encode('ascii','ignore')
##        if(is_ascii(universal.data["Name of priority country"])==False):
##            temp4=universal.data["Name of priority country"]
##            universal.data["Name of priority country"]=unicodedata.normalize('NFKD',temp4).encode('ascii','ignore')
        q = ('insert into '+universal.tablename+' values("'+
            universal.data["Application No."]+'","'+
            universal.data["Date of filing of Application"]+'","'+
            universal.data["Publication Date"]+'","'+
            universal.data["Name of Applicant"]+'","'+
            universal.data["Title of the invention"]+'","'+
            universal.data["Name of Inventor"]+'","'+
            universal.data["Abstract"]+'","'+
            universal.data["No. of Pages"]+'","'+
            universal.data["No. of Claims"]+'","'+
            universal.data["International classification"]+'","'+
            universal.data["Priority Document No"]+'","'+
            universal.data["Priority Date"]+'","'+
            universal.data["Name of priority country"]+'","'+
            universal.data["International Publication No"]+'","'+
            universal.data["International Application No"]+'","'+
            universal.data["IAFiling Date"]+'","'+
            universal.data["Patent of Addition to Application Number"]+'","'+
            universal.data["IBFiling Date"]+'","'+
            universal.data["Divisional to Application Number"]+'","'+
            universal.data["ICFiling Date"]+'")')
        universal.con.execute(q)
        universal.con.commit()
        #print(q)
    except Exception as e:
        logwriter.logwrite("MySQL: "+str(e)+"  on page "+str(int(universal.filename)+1))
        universal.logflag = 1
        Format = universal.workbook.add_format()
        Format.set_font_color('red')
        universal.worksheet.set_row(universal.row, None, Format)
