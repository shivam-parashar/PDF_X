import os
def run_command(module):
    os.system("C:/Python27/python.exe -m pip install "+module)
def printerror(module):
    print("ERROR : Could not download module "+module)
modules = ["requests","pdfminer","lxml","xlsxwriter","urllib3","PyPDF2","MySQLclient==1.3.4"]
for module in modules:
    try:
        run_command(module)
    except:
        printerror(module)

