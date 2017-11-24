from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By

driver= webdriver.Chrome("/home/killerbee/Desktop/automate/chromedriver")
#driver[l].set_window_size(10,10 , 'current')
driver.get("http://www.ipindia.nic.in/journal-patents.htm")
i=0
out=open("1.txt","w")
link1 =driver.find_elements_by_partial_link_text("Part")
while i<150:
  month =driver.find_elements_by_xpath("//table/tbody/tr["+str(i+1)+"]/td[2]")
  t_size=driver.find_elements_by_xpath("//table/tbody/tr["+str(i+1)+"]/td[5]")
  s=str(t_size[0].text)
  list_s=s.split("\n")
  out.write(month[0].text+"\n")
  j=0
  while j<len(list_s):
   out.write(str(list_s[j])+" "+str(link1[i].get_attribute("href"))+"\n")
   j+=1
  out.write("-------\n") 
  i+=1
  
driver.close()  
  


