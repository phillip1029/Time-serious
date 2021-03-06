from datetime import datetime
import pandas as pd
import simplejson as json

#Analyse all the things

def niceNumber(n):

	if n < 1000000:
		return format(int(n), ",d")
	if n > 999999 and n < 1000000000:
		return format(int(n)/1000000, ",d") + 'm'
	if n > 999999999 and n < 1000000000000:
		return format(int(n)/1000000000, ",d") + 'bn'	

def analyseData(url,source,units,entity):
	results = {}
	results["summary"] = {}

	df = pd.read_csv(url)

	allresults = df.sort_values(by='value',ascending=False).to_json(orient='records')

	# print df
	#Year trend
	gpYear = df.groupby('datetime')
	yearSum = gpYear.sum()
	yearMean = gpYear.mean()
	# print yearSum.to_json()
	results["summary"]["yearSum"] = yearSum.to_json()
	results["summary"]["yearMean"] = yearMean.to_json()

	yearPctChange = yearSum.pct_change()

	currYearPctChange = round(yearPctChange.sort_index(ascending=False)["value"].iloc[0] * 100,1)
	results["summary"]["currYearPctChange"] = currYearPctChange

	print yearSum.sort(ascending=False)["value"].iloc[0]
	mostRecentYearTotal = yearSum.sort_index(ascending=False)["value"].iloc[0]
	results["summary"]["mostRecentYearTotal"] = mostRecentYearTotal
	results["summary"]["mostRecentYearTotalStr"] = niceNumber(mostRecentYearTotal)

	# print yearSum.sort(ascending=False)["value"].iloc[0]

	mostRecentYear = yearSum.sort_index(ascending=False).index[0]
	results["summary"]["mostRecentYear"] = mostRecentYear

	mostRecentYearMean = yearMean.sort_index(ascending=False)["value"].iloc[0]
	results["summary"]["mostRecentYearMean"] = mostRecentYearMean
	
	# print mostRecentYear
	biggestEntity = df.sort_values(by="value",ascending=False)["name"].iloc[0]
	
	results["summary"]["biggestEntity"] = biggestEntity

	dfnonull = df[(df["value"] != 0) & pd.notnull(df["value"])]
	# dfnonull = dfnozeros[pd.notnull(df["value"])]

	smallestEntity = dfnonull.sort_values(by="value",ascending=True)["name"].iloc[0]
	results["summary"]["smallestEntity"] = smallestEntity

	topTen = []
	for x in xrange(0,10):
		topTen.append(df[df['datetime'] == mostRecentYear].sort_values(by="value",ascending=False)["name"].iloc[x])
			
	results["summary"]["topTen"] = topTen
		
	onlynull = df[(df['datetime'] == mostRecentYear) & pd.isnull(df['value'])]
	if len(onlynull.index) > 0:
		if len(onlynull.index) == 1:
			nullSentence = "There was only one " + entity + " that did not report in " + str(mostRecentYear) + ", which was " + str(onlynull['name'].iloc[0])
		if len(onlynull.index) > 1 :
			nullSentence = "There were " + str(onlynull.index) + " " + entity + " that did not report in " + mostRecentYear 
		results['summary']['nullSentence'] = nullSentence						

	return (results, allresults)

# analyseData('https://docs.google.com/spreadsheets/d/1l49PR88epvzcXGDReLJ-xa2DbtQmRLQN6g-SoqGgSaM/pub?output=csv','Clean Energy Regulator','tonnes of CO2 equivlaent','corporation')	
