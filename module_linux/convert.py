import commands
import universal

def run_command(string):
  if commands.getstatusoutput(string)[0]==1:
     raise NameError("ERROR IN Commands.getstatusoutput "+string)
def convert():
    #  run_command("pdf2txt.py -t html -Y exact "+"-o "+universal.filename+".html "+universal.current_dir+"/"+universal.year+"/"+universal.filename+".pdf")
  run_command("pdf2txt.py -t tag -Y exact "+"-o "+universal.current_dir+"/"+universal.tag_folder+"/"+universal.filename+universal.filename+".html "+universal.current_dir +"/"+ universal.pdf_folder+"/"+universal.filename+".pdf")
#universal.init();
#for i in range(8,622):
#  #print(i)
#  universal.filename=str(i);
#  convert() #for initializing conversion of files
    
