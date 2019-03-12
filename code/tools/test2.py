import os
from selenium import webdriver

def readJSFile(scriptFile):
    with open(scriptFile, 'r') as fileHandle:  
        script=fileHandle.read()
    return script
injectedJavascript=readJSFile("./javascriptFirefox.js")

options=webdriver.FirefoxOptions()
options.set_headless(True)
driver=webdriver.Firefox(options=options)
driver.set_script_timeout(3)

# inject JavaScript
try:
    driver.execute_async_script(injectedJavascript)
except:
    print("Timeout")

# solution found here https://stackoverflow.com/questions/17385779/how-do-i-load-a-javascript-file-into-the-dom-using-selenium
driver.execute_script("var s=window.document.createElement('script'); s.src='javascriptFirefox.js';window.document.head.appendChild(s);")
testUrl="https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html";
driver.get(testUrl)

# example sync script
time=driver.execute_script("return performance.timing.loadEventEnd - performance.timing.navigationStart;")
print(time)
# example async script
time=driver.execute_async_script("var callback = arguments[arguments.length-1]; const time = () => { total=performance.timing.loadEventEnd - performance.timing.navigationStart; callback(total); }; time();")
print(time)

file="selenium-firefox-async-script-test.png"
driver.save_screenshot(file)

driver.quit()
