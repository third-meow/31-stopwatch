'''Program for finding the time of the next 31 bus from my local bus stop'''
'''There are 11 of these bus per day and sure I could just input a list  ''' 
'''of these times but where's the fun in that?							 '''
'''																		 '''
'''By third-meow														 '''
'''Date December 2017													 '''

import urllib.request as urlr
from bs4 import BeautifulSoup as soup
from datetime import datetime


def calc_next(now_hours, now_minutes, times_hours, times_minutes):
	for i in range(0,10):
		minutes_offset = 0
		if times_hours[i] >= now_hours:
			minutes_offset = (times_hours[i] - now_hours)*60
			if times_minutes[i] > now_minutes - minutes_offset:		
				return times_hours[i], times_minutes[i]
	return times_hours[0], times_minutes[0]

				
def calc_away_time(now_hours, now_minutes, next_hours, next_minutes):
	away_hours = next_hours - now_hours
	away_minutes = next_minutes - now_minutes
	if away_minutes >= 60:
		away_hours += 1
		away_minutes -= 60
	
	elif away_minutes < 0:
		while away_minutes < 0:
				away_hours -= 1
				away_minutes += 60
	return away_minutes + (away_hours*60)
			
			
def main():
	tt = {'url':None, 
		'page':None, 
		'soup':None, 
		'times':{'box':[],
				'raw string':[],
				'string':[],
				'hours':[],
				'minutes':[],
				'next':{'hours':None,
						'minutes':None,
						'minutes away':None
						}
				}
		}
	time = {'all':None,
			'hours':None,
			'minutes':None
			}
	
	tt['url'] = 'https://www.metlink.org.nz/timetables/bus/31?date=2018-01-11'
	tt['page'] = urlr.urlopen(tt['url'])
	tt['soup'] = soup(tt['page'],'html.parser')
	
	tt['times']['box'] = tt['soup'].find_all('span',attrs={'class':'timeValue'})[:11]
	
	for b in tt['times']['box']:
		tt['times']['raw string'].append(b.text.strip())
	
	for rs in tt['times']['raw string']:
		tt['times']['string'].append(rs[:-3])
	
	for s in tt['times']['string']:
		tt['times']['hours'].append(int(s[:-3]))
		tt['times']['minutes'].append(int(s[-2:])+7)
	
	for i in range(0,10):
		if tt['times']['minutes'][i] >= 60:
			tt['times']['hours'][i] += 1
			tt['times']['minutes'][i] -= 60
		
	
	time['all'] = str(datetime.now().time())
	time['hours'] = int(time['all'][:2])
	time['minutes'] = int(time['all'][3:5])

	tt['times']['next']['hours'], tt['times']['next']['minutes'] = calc_next(time['hours'], time['minutes'], tt['times']['hours'], tt['times']['minutes'])
	
	
	tt['times']['next']['minutes away'] = calc_away_time(time['hours'], time['minutes'], tt['times']['next']['hours'], tt['times']['next']['minutes'])
	
	if tt['times']['next']['minutes away'] > 0:
		print('Next 31 bus is in'+tt['times']['next']['minutes away']+'minutes')
	else:
		print('Next 31 bus is tommorrow')
	
main()
