from redis import StrictRedis, WatchError
import os
import time
import random
import string
import json
from datetime import date

redis = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"), 
                    port=os.environ.get("REDIS_PORT", 6379),
                    db=0)

chapter_prefix = "ch14:"

olympic_stadium = {
	'venue': "Olympic Stadium",
  'capacity': 60000,
  'events': [("Athletics", "LQRW-GDOE-GZJR-KWXT"), ("Football","BERK-SGQF-FBFZ-NEVK")],
  'geo': {'long': 139.76632, 'lat': 35.666754},
  'transit': ["Toei Odeo Line", "Chuo Main Line"]
}

nippon_budokan = {
	'venue': "Nippon Budokan",
	'capacity': 12000,
	'events': [("Judo","AGHC-TXLI-ZTFN-ZHBP"), ("Karate","DDZE-PPZQ-PLNO-XBNI")],
  'geo': {'long': 139.75, 'lat': 35.693333},
  'transit':[ "Toei Shinjuku Line", "Tozai Line", "Hanzomon Line"]
}

makuhari_messe = {
	'venue': "Makuhari Messe",
	'capacity': 6000,
	'events': [("Fencing","HDSM-OJNQ-UBFZ-AKBM"), ("Taekwondo", "QTOP-FKNS-LMGQ-JHOF"), ("Wrestling","QBGH-ARMD-DFOY-JLLW")],
	'geo': {'long': 140.034722, 'lat': 35.648333},
	'transit': ["Keiyo Line"]
}

saitama_super_arena = { 
	'venue': "Saitama Super Arena",
  'capacity': 22000,
  'events': [("Basketball", "MYUD-MPRZ-RSRV-DLYM")],
  'geo': {'long': 139.630833, 'lat': 35.894889},
  'transit': ["Saitama-Shintoshin", "Takasaki Line", "Utsunomiya Line", "Keihin-Tohoku Line", "Saikyo Line"]
}

international_stadium = { 
	'venue': "International Stadium Yokohama",
  'capacity': 70000,
  'events': [("Football", "VGCM-ESPF-MXJZ-XKEX")],
  'geo': {'long': 139.606247, 'lat': 35.510044},
  'transit': ["Tokaido Shinkansen", "Yokohama Line", "Blue Line"]
}

international_swimming_center = { 
	'venue': "Tokyo Tatsumi International Swimming Center",
  'capacity': 5000,
  'events': [("Water polo","SGHI-AMGC-EFZA-RAEZ")],
  'geo': {'long': 139.818943, 'lat': 35.647668},
  'transit': ["Keiyo Line", "Rinkai Line", "Yurakucho Line"]
}

def create_venue(venue):
	p = redis.pipeline()
	p.hmset(chapter_prefix + "venues:" + venue['venue'], venue)
	p.geoadd(chapter_prefix + "venues:geo", venue['geo']['long'], venue['geo']['lat'], venue['venue'])
	p.execute()

create_venue(olympic_stadium)
create_venue(nippon_budokan)
create_venue(makuhari_messe)
create_venue(saitama_super_arena)
create_venue(international_stadium)
create_venue(international_swimming_center)

# Find venues with 5km of Tokyo Station
print redis.georadius(chapter_prefix + "venues:geo", 139.771977, 35.668024, 5, "km", withdist=True)

# Find venues within 25km of "Olympic Stadium"
print redis.georadiusbymember(chapter_prefix + "venues:geo", "Olympic Stadium", 25, "km", withdist=True)

def create_event_locations(venue):
	p = redis.pipeline()
	for i in range(len(venue['events'])):
		e, sku =  venue['events'][i]
		p.geoadd(chapter_prefix + "event:geo:" + venue['venue'], venue['geo']['long'], venue['geo']['lat'], venue['venue'])
	p.execute()

create_event_locations(olympic_stadium)
create_event_locations(nippon_budokan)
create_event_locations(makuhari_messe)
create_event_locations(saitama_super_arena)
create_event_locations(international_stadium)
create_event_locations(international_swimming_center)

# Find venues with Football within 25km of Shin-Yokohama Station
print redis.georadius(chapter_prefix + "event:geo:" + "Football", 139.606396, 35.509996, 25, "km", withdist=True)

def create_event_transit_locations(venue):
	p = redis.pipeline()
	for i in range(len(venue['transit'])):
		p.geoadd(chapter_prefix + "transit:geo:" + venue['transit'][i], venue['geo']['long'], venue['geo']['lat'], venue['venue'])
	p.execute()

create_event_transit_locations(olympic_stadium)
create_event_transit_locations(nippon_budokan)
create_event_transit_locations(makuhari_messe)
create_event_transit_locations(saitama_super_arena)
create_event_transit_locations(international_stadium)
create_event_transit_locations(international_swimming_center)

# Find venues 5km from "Tokyo Station" on the "Keiyo Line"
print redis.georadius(chapter_prefix + "transit:geo:" + "Keiyo Line", 139.771977, 35.668024, 5, "km", withdist=True)

# Find the distance between locations on the "Keiyo Line"
print redis.geodist(chapter_prefix + "transit:geo:" + "Keiyo Line", "Makuhari Messe", "Tokyo Tatsumi International Swimming Center", "km")

# Find venues within 20km of "Makuhari Messe" on the Keiyo Line
# Note: This only works if the member we are search for is on the "Keiyo Line". For example, "Olympic Statdium" is not
# so this will fail
print redis.georadiusbymember(chapter_prefix + "transit:geo:" + "Keiyo Line", "Makuhari Messe", 20, "km", withdist=True)

