import praw
# import time
import abbrevs

reddit = praw.Reddit(
  # configs for reddit bot go here.
)


def main():
    # setting the sub to parse for comments
    subreddit = reddit.subreddit("ockytop")

    # getting team abbreviations for comment parsing function
    # opponent needs changed weekly
    tennessee = abbrevs.tennessee
    opponent = abbrevs.ole_miss

    # passing lists and sub in, parsing comments for picks, returning list to main
    pick_list = read_thread(subreddit, tennessee, opponent)

    # passing picks to calc_rate to calculate pick rates for tenn and opponents
    rate_list = calc_pick_rate(pick_list)

    write_post(subreddit, pick_list, rate_list)


def read_thread(subreddit, tennessee, opponent):
    # establishing counters for picks and list to return data to main
    tennessee_counter = 0
    opponent_counter = 0
    pick_list = []

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
                    for abbreviation in tennessee:
                        if abbreviation in comment_lower:
                            tenn_status = True
                    for abbreviation in opponent:
                        if abbreviation in comment_lower:
                            opp_status = True
                    if tenn_status and not opp_status:
                        tennessee_counter += 1
                    elif opp_status and not tenn_status:
                        opponent_counter += 1
                    else:
                        continue

    # updating list with tennessee counter and opponent counter
    pick_list.append(tennessee_counter)
    pick_list.append(opponent_counter)
    return pick_list


def calc_pick_rate(pick_list):
    # creating list to hold pick rates for tenn and opponent
    rate_list = []

    # calculating total number of picks and the rate for tenn and opponent picks
    total_picks = pick_list[0] + pick_list[1]
    try:
        tenn_rate = pick_list[0] / total_picks
        tenn_rate = tenn_rate * 100
    except ZeroDivisionError:
        tenn_rate = 0
    try:
        opponent_rate = pick_list[1] / total_picks
        opponent_rate = opponent_rate * 100
    except ZeroDivisionError:
        opponent_rate = 0

    # appending data to list to return to main
    rate_list.append(tenn_rate)
    rate_list.append(opponent_rate)
    return rate_list


def write_post(subreddit, pick_list, rate_list, ut="Tennessee", opp="Opponent"):
  # posting results to the sub
  # opp needs changed weekly
    opp = "Ole Miss"
    reply_text = "" + ut + ":  " + str(pick_list[0]) + " picks {0:.2f}%".format(rate_list[0])
    reply_text += "\n \n" + opp + ":  " + str(pick_list[1]) + " picks {0:.2f}%\n \n".format(rate_list[1])
    reply_text += "State of the Sub: WGWTFA!\n \n"  # this is just a flavor saying
    reply_text += "Bloop bloop. I'm a bot. Please message u/rockytop_dev if I'm behaving badly."

    # thread title needs changed weekly
    for submission in subreddit.hot(limit=20):
        if "[Game Thread]" in submission.title:
            submission.reply(reply_text)


main()
