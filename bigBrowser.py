from tkinter import *
import hashlib
import sherlock



userBarCleaned=False
passwordBarCleaned=False
searchBarCleaned=False

page='login'

calmdown=False

def goOnline(user, password):
	global userBarCleaned
	global passwordBarCleaned
	global page
	if userBarCleaned and passwordBarCleaned:
		hashedPassword=hashlib.sha1(password.encode())
		#Envoie la requête
		print((user, hashedPassword.hexdigest()))
		if True: #Si le code est bien reçu:
			reset()
			page='web'
			load()

def cleanBar(text, bar, barName):
	if barName=='user':
		global userBarCleaned
		if not userBarCleaned:
			text.set('')
			bar.config(fg='black')
			userBarCleaned=True
	elif barName=='password':
		global passwordBarCleaned
		if not passwordBarCleaned:
			text.set('')
			bar.config(fg='black', show='*')
			passwordBarCleaned=True
	elif barName=='search':
		global searchBarCleaned
		if not searchBarCleaned:
			text.set('')
			bar.config(fg='black')
			searchBarCleaned=True
		bar.config(justify=LEFT)
	else:
		text.set('')
		bar.config(fg='black')

def uncleanBar(text, bar, barName, event=None):
	global calmdown
	global searchBarCleaned
	if event=="focusOut" and calmdown:
		calmdown=False
		return
	if event=="refreshButton" and barName=='search':
		bar.config(justify=CENTER)
		sendSearchRequest(text.get())
		searchBarCleaned=False
		return
	if text.get().replace(' ', '')=='':
		if barName=='user':
			global userBarCleaned
			if userBarCleaned:
				text.set('Pseudo')
				bar.config(fg='grey')
				userBarCleaned=False
		elif barName=='password':
			global passwordBarCleaned
			if passwordBarCleaned:
				bar.destroy()
				text.set('Mot de passe')
				createPasswordBar()
				passwordBarCleaned=False
		elif barName=='search':
			if searchBarCleaned:
				text.set(siteUrl)
				bar.config(fg='black')
				bar.config(justify=CENTER)
				searchBarCleaned=False
		else:
			text.set('...')
			bar.config(fg='grey')
	else:
		if barName=='search':
			if event!="focusOut":
				calmdown=True
				root.focus()
			bar.config(justify=CENTER)
			sendSearchRequest(text.get())



root=Tk()
root.geometry('800x400')
root.title('Big Browser')
root.minsize(600, 300)


titleFrame=Frame(root, height=20, bg='blue', padx=200, pady=4, relief='raise', bd=2)
titleFrame.pack(fill=BOTH)

title=Label(titleFrame, text='BIG BROWSER', bg='blue', font=('VERDANA BOLD',20))
title.pack(fill=BOTH)


mainFrame=Frame(root, bg='grey', padx=80, pady=40)
mainFrame.pack(expand=1, fill=BOTH)

loginFrame=Frame(mainFrame, bg='#F9F8F6', padx=30)
loginFrame.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.6)

userText = StringVar(titleFrame, value='Pseudo')
passwordText = StringVar(loginFrame, value='Mot de passe')

userBar=Entry(loginFrame, font=('VERDANA',15), fg='grey', textvariable=userText)
userBar.pack(expand=1, fill=X, side=TOP)
userBar.bind('<Return>', (lambda event: goOnline(userText.get(), passwordText.get())))
userBar.bind('<Button>', (lambda event: cleanBar(userText, userBar, 'user')))
userBar.bind('<FocusOut>', (lambda event: uncleanBar(userText, userBar, 'user')))

def createPasswordBar():
	passwordBar=Entry(loginFrame, font=('VERDANA', 15), fg='grey', textvariable=passwordText)
	passwordBar.pack(expand=1, fill=X)
	passwordBar.bind('<Return>', (lambda event: goOnline(userText.get(), passwordText.get())))
	passwordBar.bind('<Button>', (lambda event: cleanBar(passwordText, passwordBar, 'password')))
	passwordBar.bind('<FocusOut>', (lambda event: uncleanBar(passwordText, passwordBar, 'password')))
	return passwordBar

passwordBar=createPasswordBar()

goOnlineButton=Button(loginFrame, text='GO ONLINE', command=(lambda: goOnline(userText.get(), passwordText.get())), bg='#F9F8F6')
goOnlineButton.pack(expand=1, fill=BOTH, side=BOTTOM)







webFrame=Frame(root, bg='white', padx=80, pady=40)

historic=[]
siteUrl=''

def reset():
	if page=='login':
		titleFrame.destroy()
		mainFrame.destroy()
	elif page=='web':
		webFrame.destroy()

def sendRequest(request, historicNav=False):
	global webFrame
	global historic
	global siteUrl
	if True: #Si le code est bien reçu:
		reset()
		webFrame=Frame(root, bg='white', padx=80, pady=40)
		webFrame.pack(expand=1, fill=BOTH)
		siteUrl='sherlock.frd'
		website=sherlock.CODE
		exec(website)
		print(request)
		if historic[-1]!=siteUrl and (not historicNav): #si l'URL n'est pas identique à la dernière page et que nous ne sommes pas en naviguation historic
			historic.append(siteUrl)
		print(historic)


def sendSearchRequest(request):
	sendRequest(request)

def load():
	global siteUrl
	siteUrl='sherlock.frd'

	searchFrame=Frame(root, height=20, bg='grey', padx=200, pady=4, relief='raise', bd=2)
	searchFrame.pack(fill=BOTH)

	refreshImg=PhotoImage(file=r'./img/refresh.gif')

	searchText = StringVar(searchFrame, value=siteUrl)
	searchBar=Entry(searchFrame, font=('VERDANA',10), fg='black', textvariable=searchText, justify=CENTER)
	searchBar.pack(expand=1, fill=BOTH, side=LEFT)
	searchBar.bind('<Return>', (lambda event: uncleanBar(searchText, searchBar, 'search', "return")))
	searchBar.bind('<Button>', (lambda event: cleanBar(searchText, searchBar, 'search')))
	searchBar.bind('<FocusOut>', (lambda event: uncleanBar(searchText, searchBar, 'search', "focusOut")))
	searchRefreshButton=Button(searchFrame, image=refreshImg, text='refresh', highlightthickness=1, command=(lambda: uncleanBar(searchText, searchBar, 'search', "refreshButton")))
	searchRefreshButton.image=refreshImg
	searchRefreshButton.pack(side=RIGHT)

	webFrame.pack(expand=1, fill=BOTH)

	website=sherlock.CODE
	exec(website)

	historic.append(siteUrl)

	return (searchFrame, searchText, searchBar, searchRefreshButton, webFrame)
	

root.mainloop()
root.destroy()
