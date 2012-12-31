from util import hook, http

def getRank(rank):
	if "Admin" in rank:
		return "Admin"
	if "LeadMod" in rank:
		return "LeadMod"
	if "Mod" in rank:
		return "Moderator"
	if "NewMod" in rank:
		return "NewMod"
	if "Owner" in rank:
		return "Owner"
	if "Eternal" in rank:
		return "Eternal"
	if "Myth" in rank:
		return "Myth"
	if "Lgnd" in rank:
		return "Legend"
	if "Resp" in rank:
		return "Respected"
	if "Trust" in rank:
		return "Trust"
	if "New" in rank:
		return "Player"
	return "Player"

def stripTags(text):
	return ''.join(text).replace("<td>", "", 1).replace("</td>", "", 1)
	
	
@hook.command(autohelp=False)
def player(inp, nick="", reply=""):
	"player <player> --- Get DHMC Player info for <player>"

	if inp:
		nick = inp
	
	soup = http.get_soup("http://dhmc.us/players/view/%s" % nick)
	table2 = soup.find_all('table')[1]

	rank, money, orders, MCBans, joined, seen, played, country = table2.find_all('td', text=True);
	rank = rank.find_all("span")
	if "-" in joined:
		return "Player does not exist or has never joined!"
	data = {
	"nick" : nick,
	"rank" : getRank(rank[0]),
	"money" : stripTags(money),
	"orders" : stripTags(orders),
	"joined" : stripTags(joined),
	"seen" : stripTags(seen),
	"played" : stripTags(played),
	"country" : stripTags(country)
	}
	
	reply("\x02{nick}\x02 is a(n) \x02{rank}\x02 with \x02{money}\x02. " \
	"They joined \x02{joined}\x02 and were last seen \x02{seen}\x02. " \
	"They have played \x02{played}\x02 and are from \x02{country}\x02. They have filled \x02{orders}\x02 orders".format(**data));