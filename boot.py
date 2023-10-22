# boot.py -- run on boot-up
import ugit

wlan = ugit.wificonnect('Sse7en', 'kkkkkkkk')

# backup internal files
# ugit.backup() # saves to ugit.backup file

# Pull single file
# ugit.pull('file_name.ext', 'Raw_github_url')

# Pull all files
if wlan is not None:
    ugit.pull_all(isconnected=True)

