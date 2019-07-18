
import re

class Keyword :
    def __init__(self, key, link, section, section_link):
        self.key = key
        self.link = link
        self.section = section
        self.section_link = section_link
    def __str__(self):
        return "<a href=\""+ self.link + "\">" + str(self.key) + "</a>: <a href=\"" + self.section_link + "\">"+ self.section + "</a>"
    def jsonify(self):
        return str(self.key).replace("*", "\\\\*").replace("^", "\\\\^").replace("!", "\\\\!").replace(".", "\\\\.")
    def __eq__(self, other):
      return self.key==other.key
    def __hash__(self):
      return hash(('key', self.key))

# A key is uniquely defined. 
# This can be wrong, some keywords should be dupplicated due to different context
keywords = set()

fp = open("doc.html", "r")
line = fp.readline()
while not("Syntax index</h2>" in line):
  line = fp.readline()
line = fp.readline()


# Search for next h3
while (line):
  line = fp.readline()
  if "<h2" in line:
    break
  if "<tr><td></td><td valign=\"top\">" in line:
# Example line of the table :
# <tr><td></td><td valign="top"><a href="#index-_0021"><code>!</code></a>:</td><td>&nbsp;</td><td valign="top"><a href="#Operators">Operators</a></td></tr>
# General line of the table (4 var to save):
# <tr><td></td><td valign="top"><a href="#ANCHOR_TO_COMMAND"><code>KEYWORD + OPTIONS</code></a>:</td><td>&nbsp;</td><td valign="top"><a href="#ANCHOR_TO_TYPE">TYPE_OF_KEYWORD</a></td></tr>
    key = re.search(r'<code>(.*?)<', line).group(1)
    link = re.search('<tr><td></td><td valign=\"top\"><a href=\"(#[a-zA-Z0-9\-_]+)\".*', line).group(1)    
    res = re.search('nbsp;</td><td valign=\"top\"><a href=\"(#[a-zA-Z0-9\-_]+)\">([a-zA-Z0-9\-_/ ]+)</a>', line)
    section = res.group(2)
    section_link = res.group(1)

    # Delete key that are either html problem or command line option
    if(len(key) == 0 or key[0] == "-" or key[0] == "&"):
      continue
    if(section == "Command-line options"):
      continue
    if(section == "Operators" or section == "General commands" or section == "Comments"):
      continue

    # Clean key
    key = key.split("{")[0]
    key = key.split("(")[0]
    key = key.split("[")[0]
    key = key.split("\"")[0]
    #remove remaingin space
    while(key[-1] == " " or key[-1] == ";"):
      key = key[:-1]
    
    keywords.add(Keyword(key,link,section,section_link))
fp.close()

first = True
i = 0
nmax = 750
ifile = 0
fp = open("keywords_"+str(ifile)+".json", "w")
fp.write("{\n\t\t\"name\": \"keyword.gmsh\",\n\t\t\"match\":\"\\\\b(")
for k in keywords:
  i += 1
  if( i > nmax):
    i = 0
    fp.write(")\\\\b\"\n\t}")
    fp.close()
    ifile += 1
    fp = open("keywords_"+str(ifile)+".json", "w")
    fp.write("{\n\t\t\"name\": \"keyword.gmsh\",\n\t\t\"match\":\"\\\\b(")
    first = True
  if first:
    first = False
    fp.write(k.jsonify())
  else:
    fp.write("|" + k.jsonify())
fp.write(")\\\\b\"\n\t}")
fp.close()