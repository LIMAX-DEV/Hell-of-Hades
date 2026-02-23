import os
import sys

print('Check Update')
os.system('git pull')
os.system('cls' if os.name == 'nt' else 'clear')


if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


blue = "\033[0;34m"          
white = "\033[0;37m"        

print('\n')
print(blue + ' ')                                                             
                                                             
                                                             
                                                             
print('                       .=+++++++++++=.                       ')
print('                     -@@@@@@@@@@@@@@@@@-                     ')
print('                    +@@@@@@@@@@@@@@@@@@@+                    ')
print('                   +@@@@@@@@@@@@@@@@@@@@@*                   ')
print('         ...::::::#@@@@@@@@@@@@@@@@@@@@@@@%::::::...         ')
print('       .*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.       ')
print('      =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+      ')
print('     =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+     ')
print('     %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@@@@@@#:         .#@@@@@@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@@@@=      ...      =@@@@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@@@    .#@@@@@@@#.    %@@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@@.   #@@@@@@@@@@@#.  .@@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@=  .@@@@@@@@@@@@@@@.  -@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@:  .@@@@@@@@@@@@@@@.  .@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@:  .@@@@@@@@@@@@@@@.  :@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@=   =@@@@@@@@@@@@@+   =@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@@:   -@@@@@@@@@@@=.  :@@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@@@:    :@@@@@@@:    :@@@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@@@@%.             .%@@@@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@@@@@@@#.       .#@@@@@@@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%     ')
print('     %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%     ')
print('     +@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*     ')
print('      *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*      ')
print('       .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.       ')
print('         .:=*************************************=:.          ')                                                                                                   
print('      ' + white)                                                                                
print('      ' + white)                                               
                                                                                           

print(blue + '%37s' % ' [Developed By LIMAX DEV]')
print(blue + '═══════════════════════════════════════════════════════')
print(blue +'1) United States            47)Singapore')
print('2) Japan                    48) Iceland')
print('3) Italy                    49) Malaysia')
print('4) Korea                    50) Colombia')
print('5) France                   51) Tunisia')
print('6) Germany                  52) Estonia')
print('7) Taiwan                   53) Dominican Republic')
print('8) Russian Federation       54) Sloveania')
print('9) United Kingdom           55) Ecuador')
print('10) Netherlands             56) Lithuania')
print('11) Czech Republic          57) Palestinian')
print('12) Turkey                  58) New Zealand')
print('13) Austria                 59) Bangladesh')
print('14) Switzerland             60) Panama')
print('15) Spain                   61) Moldova')
print('16) Canada                  62) Nicaragua')
print('17) Sweden                  63) Malta')
print('18) Israel                  64) Trinidad And Tobago')
print('19) Iran                    65) Soudi Arabia')
print('20) Poland                  66) Croatia       ')
print('21) India                   67) Cyprus')
print('22) Norway                  69) United Arab Emirates')
print('22) Norway                  70)Kazakhstan')
print('25) Belgium                 71) Kuwait')
print('26) Brazil                  72) Venezuela')
print('27) Bulgaria                73) Georgia            ')
print('28) Indonesia               74) Montenegro') 
print('29) Denmark                 75) El Salvador      ')
print('30) Argentina               76) Luxembourg        ')
print('31) Mexico                  77) Curacao       ')
print('32) Finland                 78) Puerto Rico        ')
print('33) China                   79) Costa Rica          ')
print('34)South Africa             80) Belarus          ')
print('35) South Africa            81) Albania      ')
print('36) Slovakia                82)Liechtenstein')
print('37) Hungary                 83) Bosnia And Herzegovia')
print('38) Ireland                 84) Paraguay')
print('39) Egypt                   85) Philippines')
print('40) Thailand                86) Faroe Islands')
print('41) Ukraine                 87) Guatemala')
print('42) Serbia                  88) Nepal')
print('43) Hong Kong               89) Peru')
print('44) Greece                  90) Uruguay')
print('45) Portugal                91) Extra')
print('46) Latvia                  92)Andorra')
print('93) Antigua And Barbuda     94) Armenia  ')
print('95) Angola                  121) Laos  ')
print('96) Australia               122) Lebanon  ')
print('97) Aruba                   123) Sri Lanka')
print('98) Azerbaijan              124) Morocco')
print('99) Barbados                125) Madagascar')
print('100) Bonaire                126) Macedonia')
print('101) Bahamas                127) Mongolia')
print('102) Botswana               128) Macao')
print('103) Congo                  129) Martinique')
print('104) Ivory Coast            130) Mauritius')
print('105) Algeria                131) Namibia')
print('106) Fiji                   132) New Caledonia')
print('107) Gabon                  133) Nigeria')
print('108) Guernsey               134) Qatar')
print('109) Greenland              135) Reunion')
print('110) Guadeloupe             136) Sudan')
print('111) Guam                   137) Senegal')
print('112) Guyana                 138) Suriname')
print('113) Honduras               139) Sao Tome And Principe')
print('114) Jersey                 140) Syria')
print('115) Jamaica                141) Tanzania')
print('116) Jordan                 142) Uganda')
print('117) Kenya                  143) Uzbekistan')
print('118) Cambodia               144) Saint Vincent')
print('119) Saint Kitts            145) Benin')
print('')
print('                 120)exit             ')
import requests, re , colorama
colorama.init()
try:
    print()
    countries = ["US", "JP", "IT", "KR", "FR", "DE", "TW", "RU", "GB", "NL",
                 "CZ", "TR", "AT", "CH", "ES", "CA", "SE", "IL", "PL", "IR",
                 "NO", "RO", "IN", "VN", "BE", "BR", "BG", "ID", "DK", "AR",
                 "MX", "FI", "CN", "CL", "ZA", "SK", "HU", "IE", "EG", "TH",
                 "UA", "RS", "HK", "GR", "PT", "LV", "SG", "IS", "MY", "CO",
                 "TN", "EE", "DO", "SI", "EC", "LT", "PS", "NZ", "BD", "PA",
                 "MD", "NI", "MT", "TT", "SA", "HR", "CY", "PK", "AE", "KZ",
                 "KW", "VE", "GE", "ME", "SV", "LU", "CW", "PR", "CR", "BY",
                 "AL", "LI", "BA", "PY", "PH", "FO", "GT", "NP", "PE", "UY",
                 "-" , "AD", "AG", "AM", "AO", "AU", "AW", "AZ", "BB", 
                 "BQ", "BS", "BW", "CG", "CI", "DZ", "FJ", "GA", "GG", "GL",
                 "GP", "GU", "GY", "HN", "JE", "JM", "JO", "KE", "KH", "KN",
                 "KY", "LA", "LB", "LK", "MA", "MG", "MK", "MN", "MO", "MQ",
                 "MU", "NA", "NC", "NG", "QA", "RE", "SD", "SN", "SR", "ST",
                 "SY", "TZ", "UG", "UZ", "VC","BJ", ]
    
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:68.0) Gecko/20100101 Firefox/68.0"}


    while True:
        try:
            num_input = input(f"\n{blue}OPTIONS (1-145 or 0 to exit): {white}")
            
            if num_input == '0':
                print(f"{blue}Exiting...")
                break
                
            num = int(num_input)
            
            if num == 120:  # Opção de saída
                print(f"{blue}Exiting...")
                break
                
            if num < 1 or num > len(countries):
                print(f"{blue}Error: Please enter a number between 1 and {len(countries)}")
                continue
                
            country = countries[num-1]
            
            print(f"{blue}Fetching IPs for {country}...")
            
            res = requests.get(
                f"http://www.insecam.org/en/bycountry/{country}", 
                headers=headers,
                timeout=10
            )
            
            if res.status_code != 200:
                print(f"{blue}Error: Could not fetch data (Status code: {res.status_code})")
                continue
                
            last_page_match = re.findall(r'pagenavigator\("\?page=", (\d+)', res.text)
            
            if not last_page_match:
                print(f"{blue}No pages found for {country}")
                continue
                
            last_page = last_page_match[0]
            print(f"{blue}Found {last_page} pages")
            
            ip_count = 0
            for page in range(min(3, int(last_page))):  # Limitar a 3 páginas para performance
                try:
                    print(f"{blue}Scanning page {page + 1}...")
                    res = requests.get(
                        f"http://www.insecam.org/en/bycountry/{country}/?page={page}",
                        headers=headers,
                        timeout=10
                    )
                    
                    find_ip = re.findall(r"http://\d+\.\d+\.\d+\.\d+:\d+", res.text)
                    
                    for ip in find_ip:
                        ip_count += 1
                        print(f"{blue}{ip_count}. {ip}")
                        
                except requests.RequestException as e:
                    print(f"{blue}Error fetching page {page}: {e}")
                    continue
                    
            print(f"{blue}Total IPs found: {ip_count}")
            
            # Perguntar se quer continuar
            cont = input(f"\n{blue}Do you want to search another country? (y/n): {white}").lower()
            if cont != 'y':
                print(f"{blue}Goodbye!")
                break
                
        except ValueError:
            print(f"{blue}Error: Please enter a valid number")
        except KeyboardInterrupt:
            print(f"\n{blue}Operation cancelled by user")
            break
        except Exception as e:
            print(f"{blue}Unexpected error: {e}")
            
except KeyboardInterrupt:
    print(f"\n{blue}Program terminated by user")
except Exception as e:
    print(f"{blue}Fatal error: {e}")

finally:
    print(f"\n{white}Press Enter to exit...")
    input()