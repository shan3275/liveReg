import os
from selenium import webdriver
options=webdriver.FirefoxOptions()
options.set_headless(True)
driver=webdriver.Firefox(options=options)
# solution found here https://stackoverflow.com/questions/17385779/how-do-i-load-a-javascript-file-into-the-dom-using-selenium
driver.execute_script("var s=window.document.createElement('script'); s.src='javascriptFirefox.js';window.document.head.appendChild(s);")
driver.get('https://auth.citromail.hu/regisztracio/')
