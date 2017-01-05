# -*- coding:UTF-8 -*-

import sys
import os
import re
import urllib2
import time
from bs4 import BeautifulSoup

default_socket_timeout = 20
crawl_interval = 0.5

"""
get page content as BeautifulSoup instance
"""
def get_page(url):
	send_headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Connection':'keep-alive'
	}  	
	try:
		req = urllib2.Request(url, headers = send_headers)
		res = urllib2.urlopen(req, timeout=default_socket_timeout)
		return BeautifulSoup(res.read(), 'html.parser')
	except urllib2.HTTPError, e:
		print 'error:', url
	except:
		print 'error:', url		

"""
crawl and analyse page to get infos	
	url: info page
	keys: list of keys to analyse
"""
def analyse_baike_info(url, keys):
	soup = get_page(url)
	if not soup:
		print 'get_page error: ', url
		return []
	info = soup.find(class_ = 'basic-info cmn-clearfix')
	if not info:
		print 'analyse error: ', url
		return []
	return [get_baike_value_by_name(info, key) for key in keys]	
	
"""
extract info as text from baike page
	node:
		node in soup
	name:
		info name, an unicode
	one_level:
		extract children node text or not.	
"""
def get_baike_value_by_name(node, name):
	trans_name = u'.*'.join([c for c in name])
	text_node = node.find(text=re.compile(trans_name))
	if not text_node:
		return ''
	name_node = text_node.find_parent()
	if not name_node:		
		return ''
	value_node = name_node.find_next_sibling()
	if not value_node:
		return ''
	# extracts all element with 'target' attribute
	targets = [n for n in value_node.find_all(target='_blank')]
	if targets:
		return ','.join([strip_middle_space_and_format(n.get_text().strip()) for n in targets])
	else:
		# extracts all children to leave only text in value_node
		[n.extract() for n in value_node.find_all()]
		return strip_middle_space_and_format(value_node.get_text().strip())

"""
format patterns
"""
format_middle_delimiter_pat = re.compile(u'\s*[,，、]\s*')
format_middle_space_pat = re.compile(u'\s*')

"""
strip middle space, and 
"""
def strip_middle_space_and_format(src):	
	dest = ','.join(format_middle_delimiter_pat.split(src))
	return ' '.join(format_middle_space_pat.split(dest))
	
"""
analyse top index from soup
parameters:
	soup: BeautifulSoup instance of page
return:
	[[keyword, link, index], ...]
"""
def analyse_top_index(url):
	soup = get_page(url)
	if not soup:
		print 'analyze_top_index error: ', url
		return []
	results = []
	keywords = soup.find_all(name='td', class_='keyword')
	for keyword in keywords:
		link = keyword.find_next_sibling()
		index = link.find_next_sibling()
		top_index = [keyword.find(class_='list-title').get_text().strip(), 
			link.find(name='a').get('href'), index.get_text().strip()]
		results.append(top_index)
	return results

"""
get tops and analyse all top info
	top_url: top page
	keys: list of info keys to crawl
"""	
def crawl_all_infos(top_url, keys):
	all_infos = []
	tops = analyse_top_index(top_url)
	print 'find {0} tops in {1}'.format(len(tops), top_url)
	print '-' * 50
	for i in range(len(tops)):
		top = tops[i]
		info = analyse_baike_info(top[1], keys)
		if info:
			info.insert(1, top[2])
			all_infos.append(info)
			print 'completed {0}: {1}'.format(i + 1, top[1])
		else:
			print 'failed {0}: {1}'.format(i + 1, top[1])
		time.sleep(crawl_interval)
	print '-' * 50
	print 'completed: ' + top_url
	return all_infos

"""
save infos to file
"""	
def save_to_file(infos, file):
	with open(file, 'w') as f:
		f.writelines(['|'.join(info).encode('utf-8') + '\n' for info in infos])

"""
all tops
"""		
all_tops = {
	'movie' : ['http://top.baidu.com/buzz?b=26&c=1&fr=topcategory_c1', 'movie.txt',
		[u'中文名', u'外文名', u'其它译名', u'导演', u'编剧', u'主演', u'主要角色', u'类型', u'上映时间']
	], 
	'series' : ['http://top.baidu.com/buzz?b=4&c=2&fr=topcategory_c2', 'series.txt', 
		[u'中文名', u'外文名', u'其它译名', u'其他名称', u'导演', u'作者', u'编剧', u'主演', u'主要角色', u'类型', u'上映时间', u'播放时间', u'出版时间', u'首播时间']
	],
	'variety' : ['http://top.baidu.com/buzz?b=19&c=3&fr=topcategory_c3', 'variety.txt',
		[u'中文名称', u'外文名', u'其它译名', u'导演', u'编剧', u'主演', u'主要角色', u'类型', u'上映时间']
	],
	'anime' : ['http://top.baidu.com/buzz?b=23&c=5&fr=topcategory_c5', 'anime.txt',
		[u'中文名', u'搜索指数', u'外文名', u'外文名称', u'别名', u'原版名称', u'其他名称', u'其它译名', u'导演', u'作者', u'主持人', u'编剧', u'制片人', u'主演', u'主要角色', u'主要嘉宾',u'地区', u'类型', u'上映时间', u'播放时间', u'揭载号']
	]
}

# test_movie_url = 'http://baike.baidu.com/item/%E7%A5%9E%E6%8E%A2%E5%A4%8F%E6%B4%9B%E5%85%8B/8466957'
	
if __name__ == '__main__':
	tops = {}
	if len(sys.argv) == 2:
		key = sys.argv[1]
		tops.update({key : all_tops[key]})
	else:
		tops.update(all_tops)
	# initialize dirs
	cur_date = time.localtime()
	dir = time.strftime('data/%Y/%m/%d', cur_date)
	if not os.path.isdir(dir):
		os.makedirs(dir)	
	for key in tops:
		top = tops[key]
		infos = crawl_all_infos(top[0], top[2])
		file_name = top[1].split('.')
		time_file = '{0}/{1}-{2}.{3}'.format(dir, time.strftime('%Y%m%d', cur_date), file_name[0], file_name[1])
		save_to_file(infos, time_file)
	
