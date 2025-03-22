url = [
       "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=c1a62643-ec0e-a373-347f-14d0a91315fb&occurrenceDate=20240524",

       ]

import webbrowser

#webbrowser.open(url[0])  # Go to example.c

import mechanicalsoup
browser = mechanicalsoup.StatefulBrowser()
print(browser.open(url[0]))
browser.show()