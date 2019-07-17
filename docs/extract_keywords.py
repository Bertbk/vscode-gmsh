import re

groups = ["Group","Function","Constraint","FunctionSpace","Jacobian","Integration","Formulation","Resolution","PostProcessing","PostOperation"]

keywords = [];

fp = open("doc.html", "r")
line = fp.readline()
while not("<h2 class=\"chapter\">6 Types for objects</h2>" in line):
  line = fp.readline()
line = fp.readline()

# Search for next h3
while (line):
  line = fp.readline()
  if "<h2" in line:
    break
  if "<dt><code>" in line:
    keywords.append(line[10:-8])
fp.close()

fp = open("keywords.json", "w")
for k in keywords:
  fp.write(k + "|")
fp.close()