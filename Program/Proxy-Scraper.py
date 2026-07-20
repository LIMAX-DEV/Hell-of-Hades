from Config.Util import *
from Config.Config import *
try:
    import re
    import bs4
    import threading
    from concurrent.futures import ThreadPoolExecutor
except Exception as e:
   ErrorModule(e)
   
try:
    http = [
        {"url": "https://free-proxy-list.net/", "type": "html"},
        {"url": "https://www.sslproxies.org/", "type": "html"},
        {"url": "https://us-proxy.org/", "type": "html"},
        {"url": "https://www.socks-proxy.net/", "type": "html"},
        {"url": "https://www.proxy-list.download/api/v1/get?type=http", "type": "text"},
        {"url": "https://www.proxy-list.download/api/v1/get?type=https", "type": "text"},
        {"url": "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all", "type": "text"},
        {"url": "https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=all", "type": "text"},
        {"url": "https://www.spys.one/en/free-proxy-list/", "type": "html"},
        {"url": "https://www.hide.mn/en/proxy-list/", "type": "html"},
        {"url": "https://openproxylist.com/", "type": "html"},
        {"url": "https://www.iplocation.net/proxy-list", "type": "html"},
    ]

    socks = [
        {"url": "https://www.proxy-list.download/api/v1/get?type=socks4", "type": "text"},
        {"url": "https://www.proxy-list.download/api/v1/get?type=socks5", "type": "text"},
        {"url": "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all", "type": "text"},
        {"url": "https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all", "type": "text"},
    ]

    def GetProxyFromHtml(url):
        proxy = []
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            matches = re.findall(r'(\d{1,3}(?:\.\d{1,3}){3}):(\d{2,5})', soup.get_text())
            for ip, port in matches:
                proxy.append(f"{ip}:{port}")
        except: 
            pass

        return proxy

    def GetProxyFromText(url):
        proxy = []
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            lines = response.text.splitlines()
            for line in lines:
                line = line.strip()
                if line and re.match(r'\d{1,3}(?:\.\d{1,3}){3}:\d{2,5}', line):
                    proxy.append(line)
        except Exception as e: print(e)

        return proxy
    
    def TestProxy(max_thread, output_file, all_proxy):
        write_lock = threading.Lock()

        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                already_valid = set(line.strip() for line in f if line.strip())
        else:
            already_valid = set()

        def Test(proxy):
            proxy = proxy.strip()
            if not proxy or proxy in already_valid:
                return

            proxies = {
                "http": proxy,
                "https": proxy
            }

            try:
                response = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=20)
                if response.status_code == 200:
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Valid: {white}{proxy}")
                    with write_lock:
                        with open(output_file, 'a') as f:
                            f.write(proxy + '\n')
                            already_valid.add(proxy)
            except: pass

        to_test = [p for p in all_proxy if p.strip() and p.strip() not in already_valid]

        with ThreadPoolExecutor(max_workers=max_thread) as executor:
            executor.map(Test, to_test)

    all_proxy = []
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Selected User-Agent: {white + user_agent}")
    
    print(f"""
{BEFORE}01{AFTER}{white} Proxy Http/Https
{BEFORE}02{AFTER}{white} Proxy Socks4/Socks5
""")
    type_proxy = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Proxy type -> {reset}")

    if type_proxy not in ["1", "01", "2", "02"]:
        ErrorChoice()

    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Proxy scraping launched..")

    if type_proxy in ["1", "01"]:
        for source in http:
            url = source["url"]
            source_type = source["type"]
            if source_type == "html":
                proxy = GetProxyFromHtml(url)
            elif source_type == "text":
                proxy = GetProxyFromText(url)
            if len(proxy) != 0:
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Proxy scraped: {white}{len(proxy)}")
                all_proxy.extend(proxy)
                time.sleep(0.1)

    elif type_proxy in ["2", "02"]:
        for source in socks:
            url = source["url"]
            source_type = source["type"]
            if source_type == "html":
                proxy = GetProxyFromHtml(url)
            elif source_type == "text":
                proxy = GetProxyFromText(url)
            if len(proxy) != 0:
                print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Proxy scraped: {white}{len(proxy)}")
                all_proxy.extend(proxy)
                time.sleep(0.1)

    all_proxy = list(set(all_proxy))
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Total proxy scraped after deduplication: {white}{len(all_proxy)}")

    if type_proxy in ["1", "01"]:
        file_name = os.path.join(tool_path, "1-Output", "ProxyScraper", "Proxy_Http.txt")
    elif type_proxy in ["2", "02"]:
        file_name = os.path.join(tool_path, "1-Output", "ProxyScraper", "Proxy_Socks.txt")

    if type_proxy in ["1", "01"]:
        choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Do you want to test the proxy scraper ? (y/n) -> {reset}")
    else:
        choice = "n"

    if choice in ["Y", "y", "YES", "yes", "Yes"]:
        try:
            max_thread = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Threads (Recommended: 50) -> {reset}"))
        except: 
            Error("Invalid Number.")
        
        TestProxy(max_thread, file_name, all_proxy)
    else:
        with open(file_name, "w") as f:
            for proxy in all_proxy:
                f.write(proxy + "\n")

    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} File {white + file_name + red} created.")
    Continue()
    Reset()

except Exception as e:
    Error(e)