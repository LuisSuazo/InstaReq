import requests
import json
from bs4 import BeautifulSoup
import time
from urllib.request	import urlopen
from datetime import datetime, timedelta
import sys
import os
import os.path as path
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def obtenerData(perfil,hashtag,i):
    x = datetime.now()-timedelta(1)
    fecha = "%s-%s-%s" % (x.year, x.month, x.day)
    connect=True
    shortcode=perfil['node']['shortcode']
    with open(fecha+"_"+hashtag+".txt", i, encoding="utf-8") as f:
        try:
            req=requests.get('https://www.instagram.com/p/'+shortcode+'/')
            soup = BeautifulSoup(req.text,"html.parser")
            req.close()
            body = soup.find('body',{'class':''})
            script = body.find('script',{'type':'text/javascript'})
            data = json.loads(script.text.replace('window._sharedData = ', '')[:-1])
            f.write(json.dumps(data) + '\n')
        except:
            time.sleep(1)

def main():
    cont=0
    contadorPag=0
    hashtag=sys.argv[1]
    i=1
    b='w'
    a=True
    r = requests.get('https://www.instagram.com/explore/tags/'+hashtag+'/?__a=1')
    d = json.loads(r.text)
    endcursor=d['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
    edges=d['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    cont=cont+len(edges)
    for perfil in edges :
        obtenerData(perfil,hashtag,b)
        b='a'
    r.close()
    while(a):
        print("**********",i,"**********")
        print(endcursor)    
        i=i+1            
        if(endcursor is not None):
            conect=True
            while(conect):
                try:
                    r = requests.get('https://www.instagram.com/explore/tags/'+hashtag+'/?__a=1&max_id='+endcursor)
                    if(r.status_code == requests.codes.ok):
                        conect=False
                except:
                    r.close()
            d = json.loads(r.text)
            r.close()
            for perfil in edges :
                obtenerData(perfil,hashtag,b)
            try:
                endcursor=d['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
            except:
                a=False
        else:
            a=False
        if(i==10):
            a=False

if __name__== "__main__":
    main()
