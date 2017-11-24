import Tkinter,tkFileDialog
def browse():
  root = Tkinter.Tk()
  root.withdraw()
  filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file',filetypes = (("pdf files","*.pdf"),("all files","*.*")))
  return root.tk.splitlist(filez)
