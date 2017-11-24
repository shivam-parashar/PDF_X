#confirm identity of WIPO number
#implement sql
#implement a method to find and convert patent files of all year one by one
# -*- coding: utf-8 -*-
import difflib
from collections import namedtuple
import operator
import re
import universal
import logwriter
import unicodedata
pages_tag="No of Pages" #tags for pages and claims in whole file.
claims_tag="No of Claims"#we are using No not No. so that we can match it with No, no, 
Pair = namedtuple("Pair", ["start", "end"])
Tag = namedtuple("Tag",["tag","start","end"])
Tags=["(21) Application","Address Applicant","(22) Date filing Application","(19) India","(43) Publication Date","(54) Title Invention","(51) International classification","(31) Priority Document","(32) Priority Date","(33) Name priority country","(86) International Application","(87) International Publication","(61) Patent Addition Application","(62) Divisional Application","(71) Name Applicant","(72) Name Inventor","(57) Abstract",pages_tag, claims_tag]
indexvalues = []
flag={}#flag[tag]=1 implies value to tag has been assigned used in line 194 main usage
data = {}
probability = 0.85
reslt={}
#removes spaces and lowers the string

def burst(patent):
    words = patent.split()
    w = []
    for word in words:
        a = word.split(':')
        for b in a:
            if(b!=""):
                w.append(b.strip())
    return w;

def modify(string): 
  string="".join(burst(string)).lower()
  return string
def lcs(S,T):
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                counter[i+1][j+1] = counter[i][j]+1
            else:
                counter[i+1][j+1]=max(counter[i+1][j],counter[i][j+1])        
    return counter[m][n]
def match(word,tag):
  word=modify(word)
  tag=modify(tag)
  sq=lcs(word,tag)
  return(float(float(sq)/float(max(len(word),len(tag)))))
#this function locates expression with MINIMUM LENGTH ,similar to tag in fstring having probability atleast p0
#no restriction on arguments passed can be with or without spaces (as the match function matches the string after modifng it) 
def locate(tag,fstring,p0):  #return null for Address of applicant
  if(tag.find("Address")!=-1):
      return (-1,"")
#  if(tag.find("International Application")!=-1):
#      return (-1,"")
#  return (-1,"")    
  tag=modify(tag)
  string=""
  for x in fstring: #for converting fstring(which can be a list ) into string
    string+=x+" "
  #print(tag+" "+string)  
  p=0.0
  start=0
  end=0
  i=0
  while i <len(string):   
      j=i
      while j <i+len(tag)+8:
        arr=match(string[i:j+1],tag)
        #print(str(p)+" "+str(arr)+' '+string[i:j+1]+' '+str(i))
        if (arr>p):
          p=arr
          start=i
          end=j 
        elif(p==arr):
          p=arr
          if(end-start>=j-i):
            start=i
            end=j 
        j+=1
      i+=1
  #print(tag+" "+string[start:end+1]+" "+str(p))        
  if (start==0 and end==0) or (p<p0):
   return (-1,"") 
  return (p,string[start:end+1])     
#def locate_tags(string):
#  string=''.join(string.split()) 
#  string=string.lower()
#  for z in universal.test:
#    if locate(z,string,0.900)==-1:
#      return -1;
def matches(words, query):#returns list containing indexes of occurence of query[0] in words
    index=0
    arr = []
    while(index<len(words)):
        word =  words[index]
        s = difflib.SequenceMatcher(None, word, query)
        match = ''.join(word[i:i+n] for i, j, n in s.get_matching_blocks() if n)
        if (float(len(match)) / float(len(query)) + float(len(match)) / float(len(word)))/2  >= probability:
            arr.append(index)
        index = index+1
    return arr;

def searchtag(words,tag): #returns pair of starting and ending index of a tag in words
    tag = tag.lower()
    query = tag.split()#query(list)
    arr = matches(words,query[0]) #returns list containing indexes of occurence of query[0] in words
    index = -1 #start index variable
    index1 = -1 #end index variable
#    print(query)
#    print(words)
#    print(arr)
    for a in arr:
        i=1
        flag = True
        while i<len(query):
            array = matches(words[a+i:a+i+3],query[i])
            if(len(array)==0):
                flag = False
                break;
            if(i==len(query)-1):
                index1 = a+i+array[0]
            i = i+1
        if(flag==True):
            index = a
            break;
    #myi=input("enter")        
    return Pair(index,index1);
        
def check(words):
    if(searchtag(words,"(12) Patent Application Publication")==Pair(-1, -1)):
        return False;
    else:
        return True;

def formatdocumentno(val):      #returns value removing no. or number or no from data[tag]
    if(bool(val[0:3].lower()=="no.")|bool(val[0:3].lower()=="no,")):#no,  was found in 2017 20/01/2017
        val = val[3:].strip()#removes whitespaces from both ends
    elif(val[0:2].lower()=="no"):
        val = val[2:].strip()
    elif(val[0:6].lower()=="number"):
        return val[6:];
    if(len(val)==0):
      return "NA"    
    if(val[0]==':'):
        return val[1:].strip();
    else:
        return val.strip();

def formatabstract(val):
    i=0
    new_val=""
    for i in range(0,len(val)-1):
        if(val[i]=='"'):
            continue;
        if(bool(val[i]==' ') & (bool(val[i+1]=='.') | bool(val[i+1]==','))):
            continue;
        else:
            new_val+=val[i]
    return new_val + "."

def formatval(string):
    s = string.lower()
    if(bool(s=='-')|bool(s==':')|bool(s=='n.a')|bool(s=='n,a')|bool(s=='n.a.')|bool(s=='n/a')|bool(s=='a')|bool(s=='n,a.')|bool(s=='n.a,')|bool(s=='n,a,')|bool(s=='na')|bool(s=="nil")):
        return "NA"
    return string.strip()

def formatdate(s):
    try:
        if(s=="NA"):
            return s;
        s = s.lower().replace(',',' ').replace('.','/').replace('-','/').replace('and',' ').replace('&',' ').replace(':',' ').strip()
        Dates = s.split()
        formateddates = ''
        for Date in Dates:
            arr = Date.split('/')
            day = arr[0]
            mon = arr[1]
            year = arr[2]
            if(len(day)==1):
                day = "0" + day
            if(len(mon)==1):
                mon = "0" + mon
            if(len(mon)==3):
                mon = mon[0:2]
            if(len(year)==2):
                year = "20" + year
            formateddates += day+"/"+mon+"/"+year + " "
        return formateddates.strip()
    except:
        return "NA"

def formatfilingno(val,tag): #must return NA if val is empty
    val = formatdocumentno(val)
    val = val.lower().replace(";"," ").replace(":",' ').replace("filing",' ').replace("date",' ').replace("filed",' ').replace("on",' ').replace("and",' ').replace("&",' ').strip()
    w = val.split()
    tagval=''
    data[tag+" Filing Date"] = ''
    for s in w:
        s = formatval(s)
        if(s=="NA"):
            continue;
        if(re.search(r'^\d{2,5}\/\d{2,5}\/\d{2,5}$',s)):
            data[tag+" Filing Date"] += formatdate(s) + " "
        else:
            tagval+=s + " " 
    data[tag+" Filing Date"] = data[tag+" Filing Date"].strip()
    if(len(data[tag+" Filing Date"])==0):
        data[tag+" Filing Date"] = "NA"
    if(len(tagval)==0):
        return "NA"
    return tagval.upper().strip()
##    if(len(w)==0):
##        data[tag+" Filing Date"] = "NA"
##        return "NA"
##    else:
##        if(len(w)==1):
##          data[tag+" Filing Date"] = "NA"
##        else:
##          data[tag+" Filing Date"] = formatdate((' '.join(w[1:])).strip())
##    data[tag+" Filing Date"] = data[tag+" Filing Date"].strip()
##    return w[0].upper();

def formatstring(val):
    new_val=''
    for i in range (0,len(val)):
        if(val[i]!='"'):
            new_val += val[i]
    return new_val.strip()

def getnoofpagesandclaims(words): #what if there is numberof claims in tag ,code will assign na while this value can be extracted
    i=0
    pages = Pair(-1,-1)      #starting and ending index of tag
    claims = Pair(-1,-1)
    for i in range (0,len(words)):
        if(bool(words[i].lower()=="no.")|bool(words[i].lower()=="number")|bool(words[i].lower()=="no")|bool(words[i].lower()=="no,")):
            if(words[i+1].lower()=="of"):
                if(words[i+2].lower()=="pages"):
                    pages = Pair(i,i+2)
                elif(words[i+2].lower()=="claims"):
                    claims = Pair(i,i+2)
    return Pair(pages,claims);

def is_ascii(s):
    return all(ord(c)<128 for c in s)

def transformunicode(val):
    temp = val
    val = unicodedata.normalize('NFKD',temp).encode('ascii','ignore')
    return val

def extractvalues(words):
      indexvalues.sort(key=operator.itemgetter(1))  #sorts according to starting index
#      myi=0
#     #print(words)
#      while myi<len(indexvalues):
#       print(indexvalues[myi])
#       print(words[indexvalues[myi].start:indexvalues[myi].end+1])    #problem with abstract tag the start end values are wrong check for search tag function
#       myi+=1       
      p = 0
      while p < len(indexvalues)-1:
          if(flag[indexvalues[p].tag]!=1):
  #            print(indexvalues[p].end+1)
  #            print(indexvalues[p+1].start)
              val = (' '.join(words[indexvalues[p].end+1:indexvalues[p+1].start])).strip()
              if(len(val)>0):
                if(val[0]==':'):
                    val = val[1:]
                if(len(val)>0):
                  data[indexvalues[p].tag] = val.strip()
                else :
                  data[indexvalues[p].tag] = "NA"
              else :
                data[indexvalues[p].tag] = "NA"
              flag[indexvalues[p].tag]=1
          p = p+1
      val = ' '.join(words[indexvalues[p].end+1:])
      if(len(val)>0 and val[0]==':'):
          val = val[1:]
      if(bool(val.lower().find("continued")!=-1)&bool(val.lower().find("to")!=-1)&bool(val.lower().find("part")!=-1)):
          position = val.lower().find("continued")
          val = val[:position]
      data[indexvalues[p].tag] = val.strip()
      flag[indexvalues[p].tag] = 1
      if(flag[pages_tag]==0):
        data[pages_tag] = "NA"
      if(flag[claims_tag]==0):
        data[claims_tag] = "NA"
      for tag in data:
        if(bool(data[tag]=="")|bool(data[tag]=="na")|bool(data[tag]=="n.a.")|bool(data[tag].lower()=="nil")):
          data[tag]="NA"
        if(is_ascii(data[tag])==False):
          data[tag] = transformunicode(data[tag])
        data[tag] = formatval(data[tag])
    #if(flag["(21) Application"]!=1):
      data["(21) Application"] = formatdocumentno(data["(21) Application"])
      #if(flag["(31) Priority Document"]!=1):
      data["(31) Priority Document"] = formatdocumentno(data["(31) Priority Document"])
      #if(flag["(87) International Publication"]!=1):
      data["(87) International Publication"] = formatdocumentno(data["(87) International Publication"])
      #if(flag["(61) Patent Addition Application"]):
      data["(61) Patent Addition Application"] = formatfilingno(data["(61) Patent Addition Application"],"(61) Patent Addition Application")
      #if(flag["(62) Divisional Application"]!=1):
      data["(62) Divisional Application"] = formatfilingno(data["(62) Divisional Application"],"(62) Divisional Application")
      #if(flag["(86) International Application"]!=1):
      data["(86) International Application"] = formatfilingno(data["(86) International Application"],"(86) International Application")
      data["(54) Title Invention"] = formatstring(data["(54) Title Invention"])
    #  if(flag["(57) Abstract"]!=1): 
      data["(57) Abstract"] = formatabstract(data["(57) Abstract"])
      data["(32) Priority Date"] = formatdate(data["(32) Priority Date"])
      data["(43) Publication Date"] = formatdate(data["(43) Publication Date"])
      data["(22) Date filing Application"] = formatdate(data["(22) Date filing Application"])
      #data["(87) WIPO"]=formatdocumentno(data["(87) WIPO"])
      #if(data["(87) International Publication"]=="NA"):        #assuming WIPO=International publication
      data["(87) International Publication"]=formatdocumentno(data["(87) International Publication"])
     #if(flag["(21) Application"]!=1):        
      universal.data["Application No."] = data["(21) Application"]
     #if(flag["(22) Date filing Application"]!=1):
      universal.data["Date of filing of Application"] = data["(22) Date filing Application"]
     #if(flag["(43) Publication Date"]!=1):
      universal.data["Publication Date"] = data["(43) Publication Date"]
     #if(flag["(71) Name Applicant"]!=1):
      universal.data["Name of Applicant"] = formatstring(data["(71) Name Applicant"]) +" Address of Applicant : "   + formatstring(data["Address Applicant"])
     #if(flag["(54) Title invention"]!=1):
      universal.data["Title of the invention"] = data["(54) Title Invention"]
     #if(flag["(72) Name Inventor"]!=1):
      universal.data["Name of Inventor"] = formatstring(data["(72) Name Inventor"])
     #if(flag["(57) Abstract"]!=1):
      universal.data["Abstract"] = data["(57) Abstract"]
     #if(flag[pages_tag]!=1):
      universal.data["No. of Pages"] = data[pages_tag]
     #if(flag[claims_tag]!=1): 
      universal.data["No. of Claims"] = data[claims_tag]
     #if(flag["(51) International classification"]!=1): 
      universal.data["International classification"] = data["(51) International classification"]
     #if(flag["(31) Priority Document"]!=1):
      universal.data["Priority Document No"] = data["(31) Priority Document"]
     #if(flag["(32) Priority Date"]!=1):
      universal.data["Priority Date"] = data["(32) Priority Date"]
     #if(flag["(33) Name priority country"]!=1):
      universal.data["Name of priority country"] = data["(33) Name priority country"]
     #if(flag["(86) International Application"]!=1):
      universal.data["International Application No"] = data["(86) International Application"]
  #    if(flag["(86) International Application Filing Date"]!=1): 
      universal.data["IAFiling Date"] = data["(86) International Application Filing Date"]
     #if(flag["(87) International Publication"]!=1):
      universal.data["International Publication No"] = data["(87) International Publication"]
     #if(flag["(61) Patent Addition Application"]!=1):
      universal.data["Patent of Addition to Application Number"] = data["(61) Patent Addition Application"]
  #    if(flag["(61) Patent Addition Application Filing Date"]!=1):  
      universal.data["IBFiling Date"] = data["(61) Patent Addition Application Filing Date"]
     #if(flag["(62) Divisional Application"]!=1):
      universal.data["Divisional to Application Number"] = data["(62) Divisional Application"]
  #    if(flag["(62) Divisional Application Filing Date"]!=1):
      universal.data["ICFiling Date"]  = data["(62) Divisional Application Filing Date"]

def getdetails(new_patent):#new_patent must have spaces b/w consecutive words
    patent=""
    data.clear()
    flag.clear()
    del indexvalues[:]
    for j in range (0,len(new_patent)):
        if(new_patent[j]=='('):
          if(new_patent[j+1].isdigit()):
            patent+=" ("
        elif(new_patent[j]==')'):
          if(new_patent[j-1].isdigit()):
            patent+=") "
        else:
            patent+=new_patent[j]
    temp_patent = patent  #temp_patent is the original string with capital letters
    patent = patent.lower()
    words = burst(patent)#word(list) contains lower letter string
    if(check(words)==True):#check checks if pdf has patent
        tagindex=0
        for tag in Tags:
            flag[tag]=0#flag[tag]=1 implies value to tag has been assigned 
        pages,claims = getnoofpagesandclaims(words) #here we are going to give values to no of pages and no of claims tags and insert the starting and ending index in indexvalues
        if(bool(pages.start!=-1) & bool(pages.end!=-1)):
          indexvalues.append(Tag(pages_tag,pages.start,pages.end))#flag has been asigned 1 already in getnoofpagesandclaims
        if(bool(claims.start!=-1) & bool(claims.end!=-1)):
          indexvalues.append(Tag(claims_tag,claims.start,claims.end))#flag has been asigned 1 already in getnoofpagesandclaims
          
        while tagindex<len(Tags):
           tag=Tags[tagindex]
           if(bool(tag==pages_tag)|bool(tag==claims_tag)):
             tagindex = tagindex + 1
             continue;
           if(flag[tag]!=1): 
              i = searchtag(words,tag)#i recieve pair of tag(start,end)
              #print(tag+" "+str(words[i.start:i.end+1]))
              if(i==Pair(-1,-1)):
                  if(tag=="(87) International Publication"):
                    i = searchtag(words,"(87) WIPO")
                    if(i!=Pair(-1,-1)):
                        indexvalues.append(Tag(tag,i.start,i.end))
                        tagindex+=1
                        continue
                  if(tag[0]=='('): 
                      i = searchtag(words,tag[5:])
                      if(i!=Pair(-1,-1)):
                            indexvalues.append(Tag(tag,i.start,i.end))
                            tagindex+=1
                            continue
                  (a,b)=locate(tag,words,0.85)
                  if a!=-1:
                    i=searchtag(words,b)
                    #print(tag+" "+str(i))
                    if(i==Pair(-1,-1)):
                      data[tag]="NA" #log writer
                      logwriter.logwrite(str(tag)+" not found on page "+str(int(universal.filename)+1))
                      universal.logflag = 1
                      #print(tag)
                      flag[tag]=1
                  else :  
                   data[tag]="NA"  #log writer
                   logwriter.logwrite(str(tag)+" not found on page "+str(int(universal.filename)+1))
                   universal.logflag = 1
                   #print(tag)
                   flag[tag]=1
              #print(tag+' '+"".join(words[i.start:i.end]))   #problem with tracking of start and end index of tags  
              if(flag[tag]==0):#flag[tag]=1 implies value to tag has been assigned 
               indexvalues.append(Tag(tag,i.start,i.end))     
           #print(str(tag)+" "+str(flag[tag]))
           tagindex+=1
        #print(data)
        extractvalues(burst(temp_patent))
        return 1;
    else:
        return -1;

#patentstring="BHASKAR RAO MUKKU (57)Abstract In this system 2 pedal rods with pedals, one side balls based axle, hollowed secondary axle, counter axle, two splined gear wheels which has two clutch pin holes on circular pitch, two splined gear wheels which has ratchet gears on circular pitch, sprocket wheel, four clutch pins and a liver used to convert the ordinary bicycle into the gear bicycle. No of pages: 10"
#getdetails(patentstring)
#print(locate("No of page",patentstring,0.85)) #sometimes matches the wrong string if tag is not present in the string

