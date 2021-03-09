# Isaac Burmingham
# Code for webscraping Reddit using the praw API.

# App auth
# Only need read permission
app_id = "o57512j5W5rHmQ"
app_secret = "Eh8IVULz7v3BvRE1IY3pl73SORalHg"
app_uri = 'https://127.0.0.1:65010/authorize_callback'
app_ua = "Isaac"

reddit = praw.Reddit(client_id = app_id, client_secret = app_secret, user_agent = app_uri)

# Gets top 100 posts from each subreddit
subreddit_List = ['socialism','Conservative','denver','DenverCirclejerk','wallstreetbets','stonks','creepypasta','EmojiPasta']
dict_list = []
time_dict = {}
for subred in subreddit_List:
    start = time.time()
    # Get top 100 posts under 'all'
    for submission in reddit.subreddit(subred).top("all",limit=100):
        dat = {}
        dat["subreddit"] = subred
        dat["Post Title"] = submission.title
        dat["Post Text"] = submission.selftext
        dat["Upvotes"] = submission.score
        dat["url"] = submission.url

        # Get top 10 comments
        top_comments = list(submission.comments)
        commentList = []
        for top_level_comment in top_comments[:10]:
            commentList.append(top_level_comment.body)
        dat["comments"] = commentList
        dict_list.append(dat)
    time_dict[subred] = time.time()-start

data = pd.DataFrame(dict_list)
times = pd.DataFrame(time_dict,index=[0])
data.to_pickle('./subredditData.pkl')

times = times.transpose().reset_index().rename({'index':'Subreddit',0:'Time'},axis=1)
times.to_pickle('./Times.pkl')
