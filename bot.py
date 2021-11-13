import praw
# import time
import abbrevs

reddit = praw.Reddit(
  # configs for reddit bot go here.
)


class Team:
    """Team houses the relevant information for the team"""
    def __init__(self, name):
        self._name = name
        self._abbrevs = None
        self._count = None
        self._rate = None

    # accessors and mutators
    def get_name(self):
        return self._name

    def get_abbrevs(self):
        return self._abbrevs

    def set_abbrevs(self, team_abbrevs):
        self._abbrevs = team_abbrevs

    def get_count(self):
        return self._count

    def set_count(self, count):
        self._count = count

    def get_rate(self):
        return self._rate

    def set_rate(self, rate):
        self._rate = rate


def main():
    # setting the sub to parse for comments
    subreddit = reddit.subreddit("ockytop")

    # instances of teams
    tennessee = Team("Tennessee")
    opponent = Team("") # opponent name here

    # setting abbreviations
    tennessee.set_abbrevs(abbrevs.tennessee)
    opponent.set_abbrevs(abbrevs.opponent) # oppenent name from abbreviations list here 

    # reading thread
    read_thread(subreddit, tennessee, opponent)

    # calculating pick rates
    calc_pick_rate(tennessee, opponent)

    # writing post
    write_post(subreddit, tennessee, opponent)


def read_thread(subreddit, tennessee, opponent):
    # establishing counters for picks and list to return data to main
    tennessee_counter = 0
    opponent_counter = 0

    # iterating over submissions for predictions thread
    for submission in subreddit.hot(limit=30):
        if "[Guess the Score]" in submission.title:
            print(submission.title)
            print()
            # iterating over comments for picks
            for comment in submission.comments:
                if hasattr(comment, "body"):
                    tenn_status = False
                    opp_status = False
                    comment_lower = comment.body.lower()
                    for abbreviation in tennessee.get_abbrevs():
                        if abbreviation in comment_lower:
                            tenn_status = True
                    for abbreviation in opponent.get_abbrevs():
                        if abbreviation in comment_lower:
                            opp_status = True
                    if tenn_status and not opp_status:
                        tennessee_counter += 1
                    elif opp_status and not tenn_status:
                        opponent_counter += 1
                    else:
                        continue

    # setting pick counts for both teams
    tennessee.set_count(tennessee_counter)
    opponent.set_count(opponent_counter)


def calc_pick_rate(tennessee, opponent):

    # calculating total number of picks and the rate for tenn and opponent picks
    total_picks = tennessee.get_count() + opponent.get_count()
    try:
        tenn_rate = tennessee.get_count() / total_picks
        tenn_rate = tenn_rate * 100
    except ZeroDivisionError:
        tenn_rate = 0
    try:
        opponent_rate = opponent.get_count() / total_picks
        opponent_rate = opponent_rate * 100
    except ZeroDivisionError:
        opponent_rate = 0

    # setting rates for objects
    tennessee.set_rate(tenn_rate)
    opponent.set_rate(opponent_rate)


def write_post(subreddit, tennessee, opponent):

    # write post writes post about picks
    reply_text = "{0}: {1} picks {2:.2f}%".format(tennessee.get_name(), tennessee.get_count(), tennessee.get_rate())
    reply_text += "\n \n"
    reply_text += "{0}: {1} picks {2:.2f}%".format(opponent.get_name(), opponent.get_count(), opponent.get_rate())
    reply_text += "\n \n"
    reply_text += ""# flavor text here
    reply_text += "\n \n"
    reply_text += "Bloop bloop. I'm a bot. Please message u/rockytop_dev if I'm behaving badly."

    for submission in subreddit.hot(limit=20):
        if "Pre-Game" in submission.title:
            if tennessee.get_count() > 0 or opponent.get_count() > 0:
                submission.reply(reply_text)
                print("Jobs done!")
            else:
                print("no picks")


if __name__ == "__main__":
    main()
