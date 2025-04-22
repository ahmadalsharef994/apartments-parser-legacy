import re
str ='139 aed/ft\xb2'
value = re.search('(\d+(?:[.,]\d*)*)', str).group(1)
print(float(value.replace(',','')))