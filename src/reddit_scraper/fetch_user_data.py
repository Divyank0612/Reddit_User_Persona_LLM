import praw

class RedditUserScraper:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def get_user_profile(self, username):
        try:
            user = self.reddit.redditor(username)
            profile = {
                "name": user.name,
                "karma": {
                    "link_karma": user.link_karma,
                    "comment_karma": user.comment_karma
                },
                "cake_day": str(user.created_utc),
            }
            return profile
        except Exception as e:
            print(f"Error fetching profile for {username}: {e}")
            return None

    def get_user_submissions(self, username, limit=50):
        submissions = []
        try:
            user = self.reddit.redditor(username)
            for submission in user.submissions.new(limit=limit):
                submissions.append({
                    "title": submission.title,
                    "body": submission.selftext,
                    "subreddit": str(submission.subreddit),
                    "url": submission.url,
                    "permalink": submission.permalink,
                    "created_utc": submission.created_utc,
                })
            return submissions
        except Exception as e:
            print(f"Error fetching submissions: {e}")
            return []

    def get_user_comments(self, username, limit=50):
        comments = []
        try:
            user = self.reddit.redditor(username)
            for comment in user.comments.new(limit=limit):
                comments.append({
                    "body": comment.body,
                    "subreddit": str(comment.subreddit),
                    "link_url": comment.link_url,
                    "permalink": comment.permalink,
                    "created_utc": comment.created_utc,
                })
            return comments
        except Exception as e:
            print(f"Error fetching comments: {e}")
            return []
