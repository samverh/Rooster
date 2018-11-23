import pandas as pd
import numpy as np

rooster = pd.read_csv("schedule.csv")

# for row in rooster.iterrows():
#     for r in row:
#         print(r['Room'])
#     # for i in row:
#         # print(i)
#             # i = " - "
#     # print(row)
roooster = rooster.replace(np.nan, "")
htmlrooster = roooster.to_html()


with open("rooster1.html", 'w') as html_file:

  html_file.write("<html><head><link href='rooster.css' rel='stylesheet'/><title>TEAM TORTUGA</title></head>")
  html_file.write("<body><div><text>Rooster Team Tortuga</text></div><div>")
  html_file.write(htmlrooster)
  html_file.write("</div></body></html>")
