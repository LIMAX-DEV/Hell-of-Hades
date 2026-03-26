from Util.cfg import *
from Util.Config import *
try:
    import webbrowser
except Exception as e:
   ErrorModule(e)

Title("Info")

try:
    print(f"\n{BEFORE + current_time_hour() + AFTER} {WAIT} Information Recovery..{reset}")

    Slow(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Name Tool     :  {white}{name_tool}
 {INFO_ADD} Type Tool     :  {white}{type_tool}
 {INFO_ADD} Version       :  {white}{version_tool}
 {INFO_ADD} Creator       :  {white}{creator}
 {INFO_ADD} Platform      :  {white}{platform}
 {INFO_ADD} GunsLol  [W]  :  {white}{gunslol}
 {INFO_ADD} GitHub   [W]  :  {white}{github_tool}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
""")

    license_read = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Open 'LICENSE' ? (y/n) -> {reset}")
    if license_read in ['y', 'Y', 'Yes', 'yes', 'YES']:
        webbrowser.open_new_tab(license)
    else:
        pass
    Continue()
    Reset()
except Exception as e:
    Error(e)