import pandas as pd

rooster = pd.read_csv("schedule.csv")
htmlrooster = rooster.to_html()

with open("rooster1.html", 'w') as html_file:

  html_file.write("<html><head><link href='rooster.css' rel='stylesheet'/><title>TEAM TORTUGA</title></head>")
  html_file.write("<body><div><text>Rooster Team Tortuga</text></div><div>")
  html_file.write(htmlrooster)
  html_file.write("</div></body></html>")
