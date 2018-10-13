import requests
import json
import model_trade
import operator

trade = model_trade.Tdb()

class Markit:
	
	def __init__(self):
		self.lookup_url = "http://dev.markitondemand.com/Api/v2/Lookup/json?input="
		self.quote_url = "http://dev.markitondemand.com/Api/v2/Quote/json?symbol="

	def company_search(self,string):
		r = requests.get(self.lookup_url+string)
		print(r)
		#print(type(r))
		try:
			company_details = r.json()
			#print(type(company_details))
			return company_details
		except ValueError:
			return 0
		except KeyError:
			return 0

	def get_quote(self,string):
		r = requests.get(self.quote_url+string)
		try:
		#r.json().get("LastPrice"):
		# to access json object by key use .get
			quote = r.json()
			b = quote['LastPrice']
			alpha = [quote,b]
			return alpha
		except ValueError:
			return False
		except KeyError:
			return False

	def get_quote_update(self,string):

		r = requests.get(self.quote_url+string)
		print(r)
		try:
		#r.json().get("LastPrice"):
		# to access json object by key use .get
			quote = r.json()
			b = quote['LastPrice']
			
			return b
		except ValueError:
			return 0
		except KeyError:
			return 0

up = Markit()

def newuser(newname,newpswd):

	newuser = trade.adduser(newname,newpswd)
	return newuser

def loguser(username,userpswd):

	olduser = trade.logasuser(username,userpswd)
	return olduser

def buystock(stock_name,shares,stock_price,userid,lastprice):
	
	check_buy = trade.addstock(stock_name,shares,stock_price,userid,lastprice)
	return check_buy

def logadmin(adminname,adminpass):

	admin = trade.logasadmin(adminname,adminpass)
	return admin

def seeportfolio(userid):
	a = []
	d = []
	c = []
	u = []
	j = 0
	refresh = trade.stocknames(userid)
	for i in refresh:
		a.append(i[0])
	for i in refresh:	
		c.append(up.get_quote_update(i[0]))
	for x in refresh:
		d.append((x[1]) * c[j]) 
		j += 1
	for i in range(len(a)):
		u.append(userid)
	z = list(zip(d,a,u))
	port = trade.viewportfolio(z,userid)
	return port 

def checksym(symbol,userid):
	checksym = trade.checksymbol(symbol,userid)
	return checksym

def sellstock(stock_name,shares,stock_price,userid,lastprice):

	check_sell = trade.delstock(stock_name,shares,stock_price,userid,lastprice)
	return check_sell

def view_data_wrap():

	view_data = trade.viewallusers(updatestocks())
	return view_data


def updatestocks():
	e= 0
	g = []
	h = []
	p = []
	q = []
	stocks_name = trade.stocknames()

	for f in stocks_name:	
		g.append(up.get_quote_update(f[1]))
	for x in stocks_name:
		h.append((x[2]) * g[e])	 
		e += 1
	for r in stocks_name:
		p.append(r[0])

	q = list(zip(p,h))
	print(q)
	u = 0
	v = len(q) - 1
	result= []
	distinct = []
	#result_id = ()
	next = q
	for s in q:
		for x in s:
			if x == q[v][0]:
				result.append(x+q[v][1])
				distinct.append(x)
			v -= 1
		
	new = list(zip(distinct,result))
		#u += 1
			#for t in s:
		#print(s[0])
			#if s[0] == t[0]:
			#	result =  tuple(map(operator.add, t[1],s[1]))
			#if s[u] == t[v]:
				#result = tuple(map(operator.add, s[u],t[v]))
			#v += 1
		#u += 1
	print(new)

	#return d






