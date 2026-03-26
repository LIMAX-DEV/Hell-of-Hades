from Util.cfg import *
from Util.Config import *

try:
    import requests
except Exception as e:
    ErrorModule(e)

Title("Sql Vulnerability Scanner")

try:
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    def Xss(url):
        payloads = [
            "<script>alert('XssFound')</script>",
            "<img src=x onerror=alert('XssFound')>",
            "<svg/onload=alert('XssFound')>"
        ]
        indicators = ["<script>", "alert(", "onerror=", "<svg", "javascript:"]
        TestPayloads(url, payloads, indicators, "Xss")

    def Sql(url):
        payloads = [
            "'", '"', "''", "' OR '1'='1'", "' OR '1'='1' --", "' OR '1'='1' /*", "' OR 1=1 --", "/1000",
            "' OR 1=1 /*", "' OR 'a'='a", "' OR 'a'='a' --", "' OR 'a'='a' /*", "' OR ''='", "admin'--", "admin' /*",
            "' OR 1=1#", "' OR '1'='1' (", "') OR ('1'='1", "'; EXEC xp_cmdshell('dir'); --", "' UNION SELECT NULL, NULL, NULL --", 
            "' OR 1=1 --", "' OR '1'='1' --", "' OR '1'='1' #", "' OR '1'='1'/*", "' OR '1'='1'--", "' OR 1=1#", "' OR 1=1/*", 
            "' OR 'a'='a'#", "' OR 'a'='a'/*", "' OR ''=''", "' OR '1'='1'--", "admin' --", "admin' #", "' OR 1=1--", "' OR 1=1/*", 
            "' OR 'a'='a'--", "' OR ''=''", "' OR 'x'='x'", "' OR 'x'='x'--", "' OR 'x'='x'/*", "' OR 1=1#", "' OR 1=1--", 
            "' OR 1=1/*", "' OR '1'='1'/*", "' OR '1'='1'--", "' OR '1'='1'#", "' OR '1'='1'/*"
        ]
        indicators =  [
            "SQL syntax", "SQL error", "MySQL", "mysql", "MySQLYou",
            "Unclosed quotation mark", "SQLSTATE", "syntax error", "ORA-", 
            "SQLite", "PostgreSQL", "Truncated incorrect", "Division by zero",
            "You have an error in your SQL syntax", "Incorrect syntax near", 
            "SQL command not properly ended", "sql", "Sql", "Warning", "Error"
        ]
        TestPayloads(url, payloads, indicators, "Sql")

    def CheckPaths(url, paths, vulnerability_name):
        try:
            if not str(url).endswith("/"):
                url += "/"
            found = False
            for path in paths:
                response = requests.get(url + path, timeout=10, headers=headers)
                if response.status_code == 200:
                    found = True
                    print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Vulnerability: {white + vulnerability_name + green} Status: {white}True{green} Path Found: {white}/{path + green}")
            if not found:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Vulnerability: {white + vulnerability_name + red} Status: {white}False{red}")
        except:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Vulnerability: {white + vulnerability_name + red} Status: {white}Error during testing{red}")

    def TestPayloads(url, payloads, indicators, vulnerability_name):
        try:
            response_old = requests.get(url, timeout=10, headers=headers)
            if not str(url).endswith("/"):
                url += "/"
            found = False
            for payload in payloads:
                response = requests.get(url + payload, timeout=10, headers=headers)
                if response.status_code == 200 and response.text.lower() != response_old.text.lower():
                    for indicator in indicators:
                        if indicator.lower() in response.text.lower():
                            found = True
                            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} Vulnerability: {white + vulnerability_name + green} Status: {white}True{green} Provocation: {white + payload + green} Indicator: {white + indicator}")
                            break
            if not found:
                print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Vulnerability: {white + vulnerability_name + red} Status: {white}False{red}")
        except:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} Vulnerability: {white + vulnerability_name + red} Status: {white}Error during testing{red}")

    Slow(sql_banner)
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Selected User-Agent: {white + user_agent}")
    website_url = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Website Url -> {reset}")
    Censored(website_url)

    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Looking for a vulnerability...")
    if "https://" not in website_url and "http://" not in website_url:
        website_url = "https://" + website_url

    Sql(website_url)
    Xss(website_url)
    Continue()
    Reset()

except Exception as e:
    Error(e)

