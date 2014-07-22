QuotacleBot
===========
NOTE: This is only a snippet of the actual script because it does not include access to the database.

QuotacleBot.py is a python script that uses PRAW to grab new comments from Reddit.
It parses through them, looking to see if they are in popularquotes.txt. If so, the script generates a link to the quote on
quotacle.com and posts it as a reply.

Another script, QuotacleResponseBot.py, runs independently. This script does the same as QuotacleBot
including using the same Reddit credentials, except it finds trigger quotes (in front of the semicolon)
in quotepairs.txt, and responds with the reponse quote (behind the semicolon) in quotepairs.txt along with its 
link to quotacle.com.

Naturally, I am always changing these scripts and the libraries of quotes that they use. So what you see is not quite
what you get with /u/QuotacleBot.
