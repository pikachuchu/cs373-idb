sitemap = open("politicianhub/templates/sitemap.xml", "w")
for i in range(1, 550):
    url = "http://politicianhub.me/legislator/id/" + str(i)
    sitemap.write("\n<url>\n  <loc>" + url + "</loc>\n</url>")
for i in range(1, 228):
    url = "http://politicianhub.me/committee/id/" + str(i)
    sitemap.write("\n<url>\n  <loc>" + url + "</loc>\n</url>")
for i in range(1,311):
    url = "http://politicianhub.me/bills/id/" + str(i)
    sitemap.write("\n<url>\n  <loc>" + url + "</loc>\n</url>")
sitemap.close()
