import universal
from Tkinter import *
import commands
import os
def run_command(string):
    #print(string)
    x=commands.getstatusoutput(string)
    if x[0]==1:
       raise NameError("ERROR IN Commands.getstatusoutput "+string)
    return(x[1])   

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get() 
def makeform(root):
   entries = []
   for field in universal.data:
      row = Frame(root)
      lab = Label(row, text=field, anchor='w',height=10)
      ent = Entry(row,)
      row.pack(side=TOP, fill=X)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES)
      try:
       ent.insert(0,universal.data[field])
      except :
       zzz=1
      entries.append((field, ent))
   return entries
def fopen(tempfile):
     _file=open(universal.logfile+".txt","r").readlines()
     _page_number=0
     x=""
     x=x[:len(x)-3]
     x=x+"pdf"
     for z in _file:
      if(z.find("on page")!=-1):
       _page_number=int(z[z.find("page")+5:])
       #run_command("pdftk /media/killerbee/desktop/\"all patent files downloded\"/\"patent 2011\"/\""+x+"\" cat "+str(_page_number)+"-"+str(_page_number)+" output 3/\""+x+"\"")
       run_command("evince --page-label="+str(_page_number)+" "+tempfile)
       #print("evince --page-label="+str(_page_number)+" "+tempfile)
     #print(x)
     #x=input("en")
def init(tempfile):
     #fopen(tempfile)
     root = Tk()
     ents = makeform(root)
     root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
     b1 = Button(root, text='Show',
            command=(lambda e=ents: fetch(e)))
     b1.pack(side=LEFT, padx=5, pady=5)
     b2 = Button(root, text='Quit', command=root.quit)
     b2.pack(side=LEFT, padx=5, pady=5)
     root.mainloop()    
