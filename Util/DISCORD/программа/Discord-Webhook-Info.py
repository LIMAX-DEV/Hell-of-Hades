from Полезный.cfg import *
from Полезный.Config import *
try:
    import requests
except Exception as e:
   ErrorModule(e)
   

Title("Discord Webhook Info")

try:
    def info_webhook(webhook_url):
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.get(webhook_url, headers=headers)
        webhook_info = response.json()

        webhook_id = webhook_info.get('id', "None")
        webhook_token = webhook_info.get('token', "None")
        webhook_name = webhook_info.get('name', "None")
        webhook_avatar = webhook_info.get('avatar', "None")
        webhook_type = "bot" if webhook_info.get('type') == 1 else "webhook utilisateur"
        channel_id = webhook_info.get('channel_id', "None")
        guild_id = webhook_info.get('guild_id', "None")

        Slow(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} ID         : {white}{webhook_id}{purple}
 {INFO_ADD} Token      : {white}{webhook_token}{purple}
 {INFO_ADD} Name       : {white}{webhook_name}{purple}
 {INFO_ADD} Avatar     : {white}{webhook_avatar}{purple}
 {INFO_ADD} Type       : {white}{webhook_type}{purple}
 {INFO_ADD} Channel ID : {white}{channel_id}{purple}
 {INFO_ADD} Server ID  : {white}{guild_id}{purple}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
""")

        if 'user' in webhook_info:
            user_info = webhook_info['user']
            
            user_id = user_info.get('id', "None")
            username = user_info.get('username', "None")
            display_name = user_info.get('global_name', "None")
            discriminator = user_info.get('discriminator', "None")
            user_avatar = user_info.get('avatar', "None")
            user_flags = user_info.get('flags', "None")
            accent_color = user_info.get('accent_color', "None")
            avatar_decoration = user_info.get('avatar_decoration_data', "None")
            banner_color = user_info.get('banner_color', "None")

            Slow(f"""{purple}User information associated with the Webhook:
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} ID          : {white}{user_id}{purple}
 {INFO_ADD} Name        : {white}{username}{purple}
 {INFO_ADD} DisplayName : {white}{display_name}{purple}
 {INFO_ADD} Number      : {white}{discriminator}{purple}
 {INFO_ADD} Avatar      : {white}{user_avatar}{purple}
 {INFO_ADD} Flags       : {white}{user_flags} Publique: {user_flags}{purple}
 {INFO_ADD} Color       : {white}{accent_color}{purple}
 {INFO_ADD} Decoration  : {white}{avatar_decoration}{purple}
 {INFO_ADD} Banner      : {white}{banner_color}{purple}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    """)

    webhook_url = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Webhook URL -> {color.RESET}")
    if CheckWebhook(webhook_url) == False:
        ErrorWebhook()
    info_webhook(webhook_url)
    Continue()
    Reset()
except Exception as e:
    Error(e)