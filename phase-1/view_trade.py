import wrapper

wrap = wrapper.Markit()

def userfunctions(userlogin,userid):

	print('\n---------------')
	print('Welcome ' +userlogin+ ' !' )
	print('----------------')
	print('\nWhat would you like to do today?\n')
	#print(userid)

	options = ['Search for a company and get its stock ticker symbol ',
			   'Buy stock',
			   'Sell stock',
			   'View your current portfolio',
			   'Log out']

	index = 1
	

	for items in options:
		print(str(index) + '. ' + items)	
		index += 1

	try:
		choice = input('\nEnter your choice(1-5): ')
		choice = int(choice)
	
	except ValueError as e:
  		if not choice:
  			print("\nEmpty input!")
  		else:
  			print("\nInvalid input!")
	
	if choice == 1:
		ticker = input('\nEnter a name for the company: ')
		n = wrap.company_search(ticker)
		if not n:
			print('\nNo company found by that name')
			userfunctions(userlogin,userid)
		else:
			print('\n')
			print(n)
			userfunctions(userlogin,userid)

	elif choice == 2:
		ticker_buy = input('\nEnter the stock ticker symbol you wish to buy: ')
		symbol = wrap.get_quote(ticker_buy.upper())
		if symbol is 0:
			print('\nNo data found')
			userfunctions(userlogin,userid)
		else:
			print('\n')
			print(symbol[0])

			ans = input('\nDo you wish to buy this stock at the above mentioned last price? (Y/N): ')

			if ans.upper() == 'Y':
				shares = int(input('\nHow many shares would you like to Buy?: '))
				total_amount =  shares * symbol[1]
				buy = wrapper.buystock(ticker_buy.upper(),shares,total_amount,userid,symbol[1])
				if buy is True:
					print('\nSuccessfully bought ' + str(shares) + ' shares of ' + ticker_buy.upper())
					userfunctions(userlogin,userid)
				else:
					print('\nInsufficient Balance')
					userfunctions(userlogin,userid)

			else:
				userfunctions(userlogin,userid)

	elif choice == 3:
		portfolio = wrapper.seeportfolio(userid)
		for i in portfolio:
			print(i)
		try:
			ticker_sell = input('\nEnter the stock ticker symbol from above portfolio you wish to Sell: ')
		
		except TypeError:
			print('\nPlease enter valid input')

		#check if the stock symbol is present there in portfolio or not 
		check_sym = wrapper.checksym(ticker_sell.upper(),userid)
		if check_sym[0] == ticker_sell.upper():

			symbol_s = wrap.get_quote(ticker_sell.upper())
			if symbol_s is False:
				print('\nNo data found')
				userfunctions(userlogin,userid)
			else:
				print('\n')
				print(symbol_s[0])

				ans = input('\nDo you wish to Sell this stock at the above mentioned last price? (Y/N): ')

				if ans.upper() == 'Y':
					shares = int(input('\nHow many shares would you like to Sell?: '))
					total_amount =  shares * symbol_s[1]
			
					#check if no of shares are present in portfolio or not
					if shares <= check_sym[1]:
				
						sell = wrapper.sellstock(ticker_sell.upper(),shares,total_amount,userid,symbol_s[1])
						if sell is True:
							print('\nSuccessfully sold ' + str(shares) + ' shares of ' + ticker_sell.upper())
							userfunctions(userlogin,userid)
						else:
							print('\nInsufficient Shares')
							userfunctions(userlogin,userid)
					else:
						print('\nInsufficient Shares')
						userfunctions(userlogin,userid)

				else:
					userfunctions(userlogin,userid)

		else:
			print('\nNo data found')
			userfunctions(userlogin,userid)

	elif choice == 4:
		portfolio = wrapper.seeportfolio(userid)
		for i in portfolio:
			print(i)
		userfunctions(userlogin,userid)

	elif choice == 5:
		frontpage()

	else:
		print('\nPlease enter a valid number between 1-5')
		userfunctions(userlogin,userid)

	# except ValueError: 
	# 	print('\nEnter correct value1')
	# 	userfunctions(userlogin,userid)
	# except KeyError:
	# 	print('\nEnter correct value2')
	# 	userfunctions(userlogin,userid)
	# except NameError:
	# 	print('\nEnter correct value3')
	# 	userfunctions(userlogin,userid)
	# except TypeError:
	# 	print('\nEnter correct value4')
	# 	userfunctions(userlogin,userid)



def frontpage():

	print('\n-------------------------------')
	print('Welcome to the Trading Terminal')
	print('-------------------------------')
	options = ['Login as Admin',
			   'Login as User',
			   'Register as a New User',
			   'Exit']
	index = 1
	
	for items in options:
		print(str(index) + '. ' + items)
		index += 1
	
	

	try:
		choice = input('\nEnter your choice(1-4): ')
		choice = int(choice)
	
	except ValueError as e:
  		if not choice:
  			print("\nEmpty input!")
  		else:
  			print("\nInvalid input! ")
	

	if choice == 1:
		name = input('\nEnter username for admin: ')
		pswd = input('Enter password for admin: ')
		n = wrapper.logadmin(name.upper(),pswd.upper())
		if n is False:
			print('\n--------------------------')
			print('Wrong username or password')
			print('--------------------------')
		else:
			print('\n------------------')
			print('Logged in As Admin')
			print('------------------')	
			print('\nLeaderboard : ')
			print('--------------')

			view_data = wrapper.view_data_wrap()
			for i in view_data:
				print(i)

		frontpage()

	elif choice == 2:
		userlogin = input('\nEnter username: ')
		userpswd = input('Enter password: ')
		userid = wrapper.loguser(userlogin.upper(),userpswd.upper())
		if userlogin is False:
			print('\n--------------------------------------------')
			print('No user found or incorrect username/password')
			print('--------------------------------------------')
			frontpage()
		else:
			userfunctions(userlogin.upper(),userid) 

	elif choice == 3:
		newname = input('\nEnter a new username: ')
		newpswd = input('Enter a new password: ')
		new = wrapper.newuser(newname.upper(),newpswd.upper())
		if new is True:
			print('\n---------------------------------')
			print('Successfully added the new User')
			print('-------------------------------')
		frontpage()


	elif choice == 4:
		raise SystemExit

	else:
		print('\nPlease enter a valid number between 1-4')
		frontpage()
	
	# except ValueError: 
	# 	print('\nEnter correct value')
	# 	frontpage()
	# except KeyError:
	# 	print('\nEnter correct value')
	# 	frontpage()
	# except NameError:
	# 	print('\nEnter correct value')
	# 	frontpage()
	# except TypeError:
	# 	print('\nEnter correct value')
	# 	frontpage()

a = frontpage()

#wrapper.updatestocks()



