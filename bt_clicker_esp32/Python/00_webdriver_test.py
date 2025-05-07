from selenium import webdriver

dr = webdriver.Firefox()
wn = dr.window_handles

for w in wn:
    print(w)