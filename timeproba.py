import datetime
import re


TimestampUtc = "\/Date(1566958055158)\/"

TimestampUtc = re.split('\(|\)', TimestampUtc)[1][:10]
date = datetime.datetime.fromtimestamp(int(TimestampUtc))
print(date)
