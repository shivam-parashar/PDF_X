import datetime
f = "%d/%m/%Y"
s='07.04-2006'
s=s.replace('.','/').replace('-','/')
ss=datetime.datetime.strptime(s, f)
print(str(ss.year)+" "+str(ss.month)+' '+str(ss.day))
