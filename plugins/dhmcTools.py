from util import hook, http, text
import json, urllib2

def stripTags(text):
	text = ''.join(''.join(text).split('<td>')[0]).split('</td>')[-1]
	if "<span" in text:
		text = ''.join(''.join(text).split(">")[1]).replace("</span", "", 1)
	return text
	
def removeTags(text):
	text = ''.join(text)
	if ">" in text:
		text = text.split(">")[1].replace("</a>", "", 1)
	return text
	
def stripStrongTags(text):
	return text.replace("<strong>", "").replace("</strong>", "")

@hook.command()
def issue(inp, nick="", reply=""):
	"issue <id> -- Get the issue information for ID"
	soup = http.get_soup("https://snowy-evening.com/botsko/prism/%s" % inp)
	header = ''.join([unicode(tag) for tag in (soup.h2)])
	header = header.replace("<span>Issue Details</span>", "").replace("#%s " % inp, "")
	info = soup.find_all('p', text=True)[0]
	info = ''.join([unicode(tag) for tag in info])
	if info.isspace():
		info = "No details found"
	
	reply("Issue #%s ( https://snowy-evening.com/botsko/prism/%s ): %s - %s" % (inp, inp, header, text.truncate_str(info, 150)))
	stats = soup.find_all('ul', {'id':'stats'}, text=True)
	
	priority, number, type, status, age, somethingElse = soup.find_all('strong', text=True)
	
	data = {
	"priority" : stripStrongTags(''.join(priority)),
	"number" : stripStrongTags(''.join(number)),
	"type" : stripStrongTags(''.join(type)),
	"status" : stripStrongTags(''.join(status)),
	"age" : stripStrongTags(''.join(age))
	}
	# \x02
	reply("This issue has a priority of \x02{priority}\x02. It's age is \x02{age}\x02 and it is a \x02{type}\x02. It's status is \x02{status}\x02.".format(**data))	

@hook.command(autohelp=False)
def player(inp, nick="", reply=""):
	"player <player> --- Get DHMC Player info for <player>"

	if inp:
		nick = inp
	
	soup = http.get_soup("http://dhmc.us/players/view/%s" % nick)
	table2 = soup.find_all('table')[1]

	rank, money, orders, MCBans, joined, seen, played, country = table2.find_all('td', text=True);
	
	if "-" in joined:
		return "Player does not exist or has never joined!"
	
	data = {
	"nick" : nick,
	"rank" : stripTags(''.join([unicode(tag) for tag in rank])),
	"money" : stripTags(''.join(money)),
	"orders" : stripTags(''.join(orders)),
	"joined" : stripTags(''.join(joined)),
	"seen" : stripTags(''.join(seen)),
	"played" : stripTags(''.join(played)),
	"country" : stripTags(''.join(country))
	}
	
	reply("\x02{nick}\x02 is a(n) \x02{rank}\x02 with \x02{money}\x02. " \
	"They joined \x02{joined}\x02 and were last seen \x02{seen}\x02. " \
	"They have played \x02{played}\x02 and are from \x02{country}\x02. They have filled \x02{orders}\x02 orders".format(**data))

	
@hook.command(autohelp=False)
def listbans(inp, nick="", reply=""):
	"listbans <user> --- List a <user>'s bans on DHMC"
	if inp:
		nick = inp
	
	u = urllib2.urlopen("http://dhmc.us/api/get_bans_for_user?api_key=%s&user_id=%s&username=%s" % ("%242a%2408%24rQV01ntqvZ4vTQ6AAZTscOW.wa3b1TbLV3Xf7YVZoKWRcNRuG4Q2e", 1733, nick))
	
	bans = json.load(u)
	for ban in bans:
		
		data = {
			"nick" : ban['banned_player'],
			"id" : ban['id'],
			"date" : ban['date_created'],
			"reason" : ban['reason'],
			"mod" : ban['banning_player'],
			"unbanned" : ("not" if (ban['was_unbanned'] is 1) else "")
		}
		reply("(#{id}) {nick} is banned for \"{reason}\" by {mod}. They are {unbanned}still banned. ({date})")


@hook.command()
def stockval(inp):
	"stockval <stock> --- Get the DHMC stock value of <stock>"
	
@hook.command(autohelp=False)
def stocklist(inp, reply=""):
	"stocklist --- List DHMC's Stocks"
	
	soup = http.get_soup("http://dhmc.us/stocks")
	ul = soup.find_all('ul')[2]
	
	stocks = ""
	
	for li in ul.find_all('li'):
		name = li.find_all('a')[0]
		name = removeTags(name)
		stocks = stocks + name + ", "
	reply(stocks)
	
	
@hook.command()
def ip(inp, reply="", whois=None, channel="", nick=""):
	import json, urllib2
	# TODO support ip [username]
	# TODO config API Key
	"""if not "." in inp:
		whois(inp)
		Vars.lastChannelSentIpCommand = channel
		Vars.lastUserSentIpCommand = nick
		return None"""
	try:
		u = urllib2.urlopen("http://dhmc.us/api/joins_get_usernames_from_ip?user_id=1733&api_key=%242a%2408%24rQV01ntqvZ4vTQ6AAZTscOW.wa3b1TbLV3Xf7YVZoKWRcNRuG4Q2e&ip=" + inp)
	except urllib2.HTTPError:
		reply("An error occurred. Sorry.")
	list = json.load(u)
	if(list):
		theReply = ("Possible usernames for %s : " % inp)
		for thing in list:
			theReply = theReply + thing['username'] + ", "
		
		reply(theReply)
	else:
		reply("I do not recognize that IP.")
	"""	
@hook.event(311)
def ipUser(raw=None, privmsg=None):
	
	inp = raw.split(" ")
	ip = inp[4]
	try:
		u = urllib2.urlopen("http://dhmc.us/api/joins_get_usernames_from_ip?user_id=1733&api_key=%242a%2408%24rQV01ntqvZ4vTQ6AAZTscOW.wa3b1TbLV3Xf7YVZoKWRcNRuG4Q2e&ip=" + inp)
	except urllib2.HTTPError:
		reply("An error occurred. Sorry.")
	list = json.load(u)
	if(list):
		theReply = ("Possible usernames for %s : " % inp)
		for thing in list:
			theReply = theReply + thing['username'] + ", "
		
		privmsg("%s :(\x02%s\x02) %s" % (Vars.lastChannelSentIpCommand, Vars.lastUserSentIpCommand, theReply))
	else:
		privmsg("%s :(\x02%s\x02) I do not recognize that IP." % (Vars.lastChannelSentIpCommand, Vars.lastUserSentIpCommand))
	
class Vars():
	lastUserSentIpCommand = "Person"
	lastChannelSentIpCommand = "#dhmc_us"
	"""