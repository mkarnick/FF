import yahoo.yql

response = yahoo.yql.YQLQuery().execute('select * from fantasysports.games where game_key="238"')
if 'query' in response and 'results' in response['query']:
 	print response['query']['results']
elif 'error' in response:
 	print 'YQL query failed with error: "%s".' % response['error']['description']
else:
 	print 'YQL response malformed.'


 	https://query.yahooapis.com/v1/public/yql?q=show%20tables&format=json&diagnostics=true&callback=