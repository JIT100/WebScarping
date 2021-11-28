import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
from itertools import cycle
import json

proxyList = []

def decoder(EncodedIP):
    txt= EncodedIP
    js = re.search(r"%3c.*\b", txt).group()
    encoded=re.split('"\)',js)
    decoded = urllib.parse.unquote(encoded[0])
    IP = re.split("[><]",decoded)
    return IP[2]


def proxies():
    urls = ["https://www.freeproxylists.net/?page=2","https://www.freeproxylists.net/?page=1",]
    
    headers2={'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.52',"cookie": 'hl=en; userno=20210309-014019; from=direct; __gads=ID=83e516c65420001e-221168d04bc60064:T=1615301678:RT=1615301678:S=ALNI_MYY48XZVhhEQfkKmgt6xEJNpcXVFA; __atssc=google%3B1; visited=2021%2F11%2F27+15%3A49%3A43; __utmz=251962462.1637995783.4.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; __utma=251962462.1341350947.1615301676.1638025911.1638091846.11; __utmc=251962462; __utmt=1; __utmv=251962462.France; pv=26; __atuvc=0%7C44%2C0%7C45%2C0%7C46%2C15%7C47%2C4%7C48; __atuvs=61a34c46329feacf003; __utmb=251962462.8.10.1638091846'}
    headers1={'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.52','cookie': 'hl=en; userno=20210309-014019; from=direct; __gads=ID=83e516c65420001e-221168d04bc60064:T=1615301678:RT=1615301678:S=ALNI_MYY48XZVhhEQfkKmgt6xEJNpcXVFA; __atssc=google%3B1; visited=2021%2F11%2F27+15%3A49%3A43; __utmz=251962462.1637995783.4.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; __utma=251962462.1341350947.1615301676.1638025911.1638091846.11; __utmc=251962462; __utmt=1; __utmv=251962462.France; pv=27; __atuvc=0%7C44%2C0%7C45%2C0%7C46%2C15%7C47%2C5%7C48; __atuvs=61a34c46329feacf004; __utmb=251962462.10.10.1638091846'}
    headers=[headers1,headers2]
    for i in range(0,2):
        r = requests.get(urls[i],headers=headers[i])
        #print(urls[i])
        print(r.status_code)
        #print(r)
        S = BeautifulSoup(r.content, "html.parser")
        #print(S)

        for x in S.find("table",{"class":"DataGrid"}).find_all("tr")[1:]:
            tds = x.find_all("td")
            try:
                if (tds[4].text.strip()) == "United States":
                    #print(tds[4].text.strip())
                    x=str(tds[0])
                    IP=decoder(x)
                    #print(IP)
                    PORT = tds[1].text.strip()
                    Location = tds[4].text.strip()        
                    host = "{}:{}".format(IP, PORT)
                    proxyList.append(host)                               
            except IndexError:
                continue
    return proxyList

def WebScrap(url,proxyList, **kwargs):
    proxy_pool = cycle(proxyList)
    k = 0
    for i in range(len(proxyList)): 
            if i==len(proxyList)-1:
                print("None of the proxies are online")
                txt=str(input("Do you wanna run the program again? Type: yes/no"))
                if txt=="yes":
                    res=WebScrap(URL,proxyList)
                    print(res)
                else:
                    print("program has been closed")
            else:
                proxy = next(proxy_pool)
                k+=1
                print(f"Request #{k}")
                try:
                    print(f"Using '{proxy}'IP address for  scrapping, ID {k}")
                    headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.52","cookie":'_ga=GA1.2.1205362738.1615301639; __pr.dgt=_IEcX3_tqz; ASP.NET_SessionId=gv5atnex3zxgpvsawzobnrbw; _gid=GA1.2.444593488.1638086130; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1'}
                    response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=10,headers=headers, **kwargs)
                    soup= BeautifulSoup(response.content, "html.parser")
                    #print(soup)
                    ID=0
                    Product={}
                    for x in soup.find_all("div",class_="product"):
                        ID+=1
                        serial_no=f"Product {ID}"
                        tittle=x.find("a",class_="catalog-item-name")
                        y=x.find("span",class_="price")
                        z=x.find("span",class_="status")
                        #print("ID=",ID, "Tittle:   " , tittle.text ,"and", "price:  ", y.text,"and", "status:  ",z.text)
                        Product[serial_no]=["Name" , tittle.text,"Price",y.text,"Status", z.text]
                    js=json.dumps(Product,indent=5)
                    #print(js)
                    return js


                except:
                    print("Connection error,looking for new IP")
                    pass

URL = "https://www.midsouthshooterssupply.com/dept/reloading/primers?itemsperpage=90"

proxyList=proxies()
res=WebScrap(URL,proxyList)
print(res)