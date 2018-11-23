"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program visualizes the CSV output made by main.py via a webpage.
"""

import pandas as pd
import numpy as np

# import csv file containing schedule and replace empty values by empty string
rooster = pd.read_csv("schedule.csv").replace(np.nan, "")

# convert the dataframe to an html formatted table
htmlrooster = rooster.to_html()

# write an html file and insert the table
with open("rooster.html", 'w') as html_file:

    html_file.write("<html>\n  <head>\n\
      <link href='rooster.css' rel='stylesheet'/>\n\
      <title>TEAM TORTUGA</title>\n  </head>\n")
    html_file.write("  <body>\n    <div><text>Rooster Team Tortuga</text></div>\n\    <div>\n")
    html_file.write(htmlrooster)
    html_file.write("\n</div>\n</body>\n</html>")
