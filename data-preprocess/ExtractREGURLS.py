from bs4 import BeautifulSoup
import urllib.request, re, wget

WebPageHTMLSource = urllib.request.urlopen("https://www.panynj.gov/airports/traffic-statistics.html")
soup = BeautifulSoup(WebPageHTMLSource, "html.parser")

i=0 # debug code used to count number of results captured by regex

for links in soup.find_all("a", href=re.compile("REG", re.IGNORECASE)):
  i+=1 # debug code used to count number of results captured by regex
  print(links['href']) # debug code
  # wget.download("https://www.panynj.gov/" + links['href'], out="AirlinePDFs/")

### Note that due to the poor naming scheme used by this site, the Dec 2004 file name isn't captured by the previous regex expression
  # i+=1 # debug code used to count number of results captured by regex
  print('value of i is ' + str(i)) # debug code
# wget.download("https://www.panynj.gov/airports/pdf-traffic/Dec_2004.pdf", out="AirlinePDFs/")

