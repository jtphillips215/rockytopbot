# rockytopbot

Rockytop bot parses the weekly "Guess the Score" thread and posts the results to the sub in either the pregame or game threads.

It uses PRAW to access reddit, parses the "Guess the score" thread comments for commands (in abbrevs), calculates the number of picks and pick rate, and then posts the results.

Each week the opponent must be updated so that the new abbreviations are pulled in

Additionally, the flavor text can be changed each week to something of interest around the program.
