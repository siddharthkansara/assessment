import sqlite3

class Tdb:
	
	def __init__(self):

		self.conn = sqlite3.connect('trade_db.db')
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_name varchar(30) NOT NULL, password varchar(30) NOT NULL, total_balance REAL DEFAULT 100000.00);")
		self.cur.execute("CREATE TABLE IF NOT EXISTS stocks(id INTEGER , stock_name varchar(30) NOT NULL, quantity INTEGER NOT NULL, last_price REAL NOT NULL,total_value REAL NOT NULL);")
		self.conn.commit()
		
	def adduser(self,name,pswd):

		self.conn = sqlite3.connect('trade_db.db')
		self.cur = self.conn.cursor()
		self.cur.execute("INSERT INTO users(user_name,password) VALUES(?,?);",[name,pswd])
		self.conn.commit()
		return True

	def logasadmin(self,username,pswd):
		self.conn = sqlite3.connect('trade_db.db')
		self.cur = self.conn.cursor()					
		if username == 'ADMIN' and pswd == 'ADMIN':
			return True
		else:
			return False

	def logasuser(self,uname,userpswd):

		self.conn = sqlite3.connect('trade_db.db')
		self.cur = self.conn.cursor()	
		self.cur.execute("SELECT id from users WHERE (user_name = (?)) AND (password = (?)) ;",[uname,userpswd])
		self.conn.commit()
		user_id = self.cur.fetchone()[0]
		if user_id is not None:
		 	return user_id
		else:
			return False

	def addstock(self,stock,quan,stockprice,userid,lastprice):

		self.conn = sqlite3.connect('trade_db.db')
		self.cur = self.conn.cursor()	
		self.cur.execute("SELECT total_balance from users where (id = (?));",[userid])
		self.conn.commit()
		check = self.cur.fetchone()[0]

		if check >= stockprice:
			self.cur.execute("SELECT stock_name from stocks WHERE stock_name = (?);",[stock])
			if self.cur.fetchone() is not None:
				
				self.cur.execute("SELECT quantity from stocks WHERE id = (?) AND (stock_name = (?));",[userid,stock])
				old_quan = self.cur.fetchone()[0]
				new_quan = old_quan + quan
				self.cur.execute("UPDATE stocks SET quantity = (?) WHERE id = (?) AND (stock_name = (?));",[new_quan,userid,stock])
				self.conn.commit()
			
			else:

				self.cur.execute("INSERT INTO stocks(id,stock_name,quantity,last_price,total_value) VALUES(?,?,?,?,?);",[userid,stock,quan,lastprice,stockprice])
				self.conn.commit()
				new_bal = check - stockprice
				self.cur.execute("UPDATE users SET total_balance = (?) WHERE (id = (?));",[new_bal,userid])
				self.conn.commit()
				self.conn.close()

			return True

		else:
			return False

	def viewportfolio(self,d,userid):

		self.conn = sqlite3.connect('trade_db.db')
		self.cur = self.conn.cursor()
		to_db = [(x,y,z) for (x,y,z) in d]
		self.cur.executemany("UPDATE stocks SET total_value = (?) WHERE (stock_name = (?) AND id = (?));",to_db)
		self.cur.execute("SELECT * from stocks WHERE (id = (?) AND quantity != 0 );",[userid])
		list_stock = self.cur.fetchall()
		self.conn.commit()
		self.conn.close()
		return list_stock

	def delstock(self,stock,quan,stockprice,userid,lastprice):

		self.conn = sqlite3.connect('trade_db.db')
		self.cur = self.conn.cursor()	
		self.cur.execute("SELECT quantity,stock_name from stocks where id = (?) AND (stock_name = (?));",[userid,stock])
		self.conn.commit()
		check = self.cur.fetchone()

		if quan <= check[0] :
			new_quan = check[0] - quan
			self.cur.execute("UPDATE stocks SET quantity = (?) WHERE id = (?) AND (stock_name = (?)) ;",[new_quan,userid,stock])
			self.conn.commit()
			self.cur.execute("SELECT total_balance from users WHERE (id = (?));",[userid])
			self.conn.commit()
			last_bal = self.cur.fetchone()[0]
			new_bal =  stockprice + last_bal
			self.cur.execute("UPDATE users SET total_balance = (?) WHERE (id = (?));",[new_bal,userid])
			self.conn.commit()
			self.cur.execute("SELECT total_value from stocks WHERE id = (?) AND (stock_name = (?));",[userid,stock])
			last_value = self.cur.fetchone()[0]
			new_value = last_value - stockprice
			self.cur.execute("UPDATE stocks SET total_value = (?) WHERE id = (?) AND (stock_name = (?));",[new_value,userid,stock])
			self.conn.commit()
			self.conn.close()

			return True
		else:
			return False
		

	def checksymbol(self,stock,userid):

		self.conn = sqlite3.connect('trade_db.db')
		self.cur = self.conn.cursor()
		self.cur.execute("SELECT stock_name, quantity from stocks WHERE id = (?) AND (stock_name = (?));",[userid,stock])
		check = self.cur.fetchone()
		self.conn.commit()
		self.conn.close()
		if check is not None:
			return check
		else:
			return False

	def viewallusers(self,d):

		self.conn = sqlite3.connect('trade_db.db')
		self.cur = self.conn.cursor()

		self.cur.execute("SELECT users.id, users.user_name,stocks.total_value FROM users,stocks WHERE (users.id = stocks.id);")
		check = self.cur.fetchall()

		return check

	def stocknames(self,userid):

		self.conn = sqlite3.connect('trade_db.db')
		self.cur = self.conn.cursor()
		self.cur.execute("SELECT stock_name,quantity,id from stocks;")
		names = self.cur.fetchall()

		return names

























			