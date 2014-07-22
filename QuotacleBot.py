""" Go to line 80 for interesting suff """
import praw
import datetime
import time
import sys, os
import uuid
def simplifyText(string):
	string=string.lower()
	contractions = [("can't","cannot"), ("i'm","i am"), ("you're","you are"), ("don't","do not"), ("i'll","i will"), ("you'll","you will"), ("he'll","he will"), ("she'll","she will"), ("they'll","they will"), ("it'll","it will"), ("it's","its"), ("he's","he is"), ("she's","she is"),("where'd","where did"),("that's","that is")]
	for contraction in contractions:
		string = string.replace(contraction[0], contraction[1])
	slang = [("naw","no"),("favourite","favorite"),("colour","color"),("armour","armor"),("wanna","want to"),("gonna","going to"),("outta","out of")]
	for phrasePair in slang:
		string = string.replace(phrasePair[0], phrasePair[1])
	for word in string.split():
		if word[-1] == "'":
			string = string.replace("'","g")
	for ch in ['"', "'", ',', ':', '.', '!']:
		string=string.replace(ch,"")
	for ch in ['-']:
		string=string.replace(ch," ")
	string=string.strip()
	return string
	
def custom_search(commentString):
	replacepairs = [("that is no moon that is a death star","that is no moon"),("that is a tasty burger","this is a tast burger"),("no i am your father","i am your father"),("i do not mean to pry but you do not by any chance happen to have six fingers on your right hand","by any chance happen to have"),("that is no moon that is a space station","that is no moon")]
	for replacepair in replacepairs:
		if commentString == replacepair[0]:
			return replacepair[1]
	return commentString
	
def is_not_common(quote):
	commonPhrases = ["what do you think","i do not believe you","what is the point","no thank you","you know I do","i do not know","i will be there","what do you want","if you are good","what do you mean","you cannot be serious","it is not a question","what do you do","i think it is","i think it is time","the way I see it","i do not want to kill you","you do not need to","what are you going to do","i do not know how to put this","i do not know how","surely you cannot be serious","what is your favorite color","i have to go","i have to go to"]
	for phrase in commonPhrases:
		if simplifyText(quote) == simplifyText(phrase):
			return False
	return True
	
def is_not_banned_subreddit(subreddit):
	for badsubreddit in ["obert_paulson","askreddit","leagueoflegends"]:
		if subreddit == badsubreddit:
			print("Banned subreddit: " + subreddit)
			return False
	return True
	
def word_in (word, phrase):
    return word in phrase.split()
    
def phrase_in(needle_string, haystack_string):
	haystackList = haystack_string.split(";")
	if haystack_string.find(needle_string) != -1:
		for haystackPhrase in haystackList:
			if haystackPhrase.find(needle_string) != -1:
				startpos = haystackPhrase.find(needle_string)
				nextCharPos = startpos + len(needle_string)
				prevCharPos = startpos - 1
				try:
					if haystackPhrase[nextCharPos].isalpha():
						return False
				except IndexError:
					pass
				if prevCharPos != -1:
					try:
						prevChar = haystackPhrase[prevCharPos]
						if prevChar.isalpha():
							return False
					except IndexError:
						pass			
				return True
	return False
		
with open("popularquotes.txt") as myfile:
	txtlines = myfile.read().splitlines()

r = praw.Reddit('Quote finder by u/QuotacleBot')
r.login('QuotacleBot', '*******')
user = r.get_redditor('QuotacleBot')
already_done = set()
numUniqueComments = 1
while True:
	try:
		all_comments = r.get_comments('all', limit=100)
		for comment in all_comments:
			if comment.id in already_done:
				time.sleep(5)
				break
			else:
				if(len(simplifyText(comment.body)) > 10 and len(simplifyText(comment.body).split()) >= 5 and len(simplifyText(comment.body)) < 200):
					for txtline in txtlines:
						txtlineList = txtline.split(';')
						title = txtlineList[0]
						quotesList = txtlineList[1:]
						quotesString = ';'.join(quotesList)
						if phrase_in(simplifyText(comment.body), simplifyText(quotesString)):
							comment.body = custom_search(comment.body)
							if is_not_common(simplifyText(comment.body)):
								if is_not_banned_subreddit(comment.subreddit.display_name):
									# Create link to quotacle.com
									break
						
				numUniqueComments = numUniqueComments + 1
				if numUniqueComments % 1000 == 0:
					print(numUniqueComments)
			already_done.add(comment.id)
		# Delete comments with -1 karma
		for comment in user.get_comments():
			if ((comment.ups - comment.downs) <= -1):
				comment.delete()
				print("Comment deleted " + comment.permalink)
				time.sleep(5)
		
	except:
		# Error reporting
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		time.sleep(10)



