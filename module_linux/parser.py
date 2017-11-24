#using tag for fields in pdf for which information is to be extracted and value for information 
from lxml import html
import need
import universal
import logwriter
import extractor
def reopen(filename):                           #open the html file for parasing
  requests_session = need.requests.session()
  requests_session.mount('file://', need.LocalFileAdapter())
  page = requests_session.get('file://'+universal.current_dir+"/"+universal.tag_folder+"/"+filename)   #file name
  universal.tree = html.fromstring(page.content)
#def extractor(index,tag) :
# data from html file--> abcdaaa
# tag         ---------> axabcydaa
#Approach A1
#now what we know is that the tag is complete and a subsequence of tag will be the data from html file ....but if we use s.get_matching_blocks() it returns the longest common subsequence which will be wrong consider
#Approach A2
# data from html file--> international_total_publication
# tag         ---------> international publication 
#this will match while they are two different tags so...we cant use this approach 
#my approach:-
#remove all the whitespaces from the universal.datastring and then we will use the approach A1 to extract tags from universal.datastring
def begin():      #return 1 if string is not present
  universal.datastring=""
  reopen(universal.filename+universal.filename+".html") #html-tag filename converted from pdf
  #page = requests_session.get('file:///home/killerbee/Desktop/test2/'+filename)   #file name
  #universal.tree = html.fromstring(page.content)
  s=universal.tree.itertext()
#  universal.test=["(21) Application No","Date of filing of Application","Publication Date","Title of the invention","International classification","Priority Document","Priority Date","Name of priority country","International Application","Fil","International Publication","Patent of Addition to Application","Fil","Divisional to Application","Fil","Name of Applicant","(72)Name of Inventor","Abstract"]
  logwriter.logwrite("***************"+universal.filename+"*************")
  for a in s:
    universal.datastring+=a
  try :  
   return(extractor.getdetails(universal.datastring))
      
 
  except Exception as e:
   logwriter.logwrite(e) 
   return -1
#  write code for case when tayal returns -1 and you have to run your extraction function 
#  implement ur extraction function and then call it 
  
  
  
  
  
  
  
  
  
  
  
  
  #extractor.getdetails(universal.datastring)
#  for tag in universal.test:
#    tempi=i
#   # i=extractor(i,tag)
#    if i==-1:
#      if(extractor.mycheck(universal.datastring)==0):
#        fappend=open("log.txt",'a')
#        fappend.write("-->"+str(universal.filename)+"->"+tag+"--->"+universal.datastring[tempi:tempi+len(tag)]+'\n')
#        fappend.close()
#        return -1
#    i+=1 
  
  return 0
