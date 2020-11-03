from urllib.parse import urlparse

parsed = urlparse("https://mswe.ics.uci.edu/admissions/cost-and-financial-aid")

print(parsed[0]+" "+parsed[1])