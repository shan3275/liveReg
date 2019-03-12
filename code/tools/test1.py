from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
#options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

#w = webdriver.Chrome(executable_path="/Applications/chromedriver",chrome_options=options)
w = webdriver.Chrome(executable_path="/Applications/chromedriver")
w.execute_script("var s=window.document.createElement('script'); s.src='javascriptFirefox.js';window.document.head.appendChild(s);")
w.get('http://www.ivolatility.com/')
