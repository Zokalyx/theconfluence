import random
import DbHandler
from queue import Queue
from praw import Reddit
from praw.models import Submission, Redditor, Comment, Subreddit, MoreComments
from typing import Iterator, Optional, Tuple


class RedditorInfo:
    """
        Special class that holds useful information about
        a new redditor and where it was found
    """

    def __init__(
            self, name: str, sub: str, postId: str, isOp: bool, commentId: Optional[str] = None):
        """
            Creates an instance, which holds the data passed in

            `name` is the username

            `sub` is the subreddit in which the user was found

            `postId` is the id of the post in which the user was found

            `commentId` is the id of the comment in which the user was found (if any)

            `isOp` represents if the user is the OP of the post or not
        """
        self.name = name
        self.sub = sub
        self.postId = postId
        self.isOp = isOp
        self.commentId = commentId


class RedditorQueue(Queue):
    """
        Queue containing a certain amount of `RedditorInfo`s
    """
    def __init__(
        self,
        maxsize: int,
        reddit: Reddit,
        blacklist: Optional[list[str]] = [],
        allowNsfw: Optional[bool] = False
    ) -> Queue[RedditorInfo]:
        """
            Creates a RedditorQueue

            `maxsize` indicates the maximum size of the queue

            `reddit` is the instance that will be used to
            select random redditors
        """
        self.reddit = reddit
        self.blacklist = blacklist
        self.allowNsfw = allowNsfw
        self.db = DbHandler.DbHandler()
        super().__init__(maxsize)

    def generator(self) -> Iterator[str]:
        """
            Returns a generator over all redditors in queue

            If generator is iterated over, queue gets cleared
        """
        while not self.empty():
            yield self.get()

    def fill(self, minAmount) -> None:
        """
            Fills this queue until there are a minimum amount of redditors in it

            Ideally, this would do nothing because the queue is already full. But
            there might be situations in which the queue is not ready
        """
        # Prevent infinite loops
        if minAmount > self.maxsize:
            minAmount = self.maxsize
        # Fill
        while self.qsize() < minAmount:
            self.cycle()

    def cycle(self) -> None:
        """
            Finds a random redditor to add to the queue

            If queue is full, pop a redditor from the queue
        """
        # Try a certain amount of times
        for i in range(10):
            try:
                redditor = self.getRedditor()
                break
            except Exception as e:
                print(e)
        # Once redditor info was successfully obtained, add it
        if self.full():
            self.get()
        self.put(redditor)

    def startCycling(self, frequency) -> None:
        """
            Starts automatically cycling, based on the passed frequency

            TODO: Implement. What is the best approach to this?
        """
        raise NotImplementedError

    def stopCycling(self) -> None:
        """
            Stops automatically cycling

            TODO
        """
        raise NotImplementedError

    def getRedditor(self) -> RedditorInfo:
        """
            Implements the algorithm to find a random redditor
        """

        try:
            sub, category = self.getRandomSub()
            post, pickOp = self.getRandomPost(sub, category)
        except Exception as e:
            raise e

        if pickOp:
            redditor = post.author
        else:
            redditor, pickOp, commentId = self.getRandomCommenter(post)

        if not redditor:
            raise Exception("Redditor account unavailable")
        elif redditor.name in self.blacklist:
            raise Exception("Redditor in blacklist")
        elif self.checkMembership(redditor.name):
            raise Exception("Redditor already in The Confluence")

        return RedditorInfo(redditor.name, sub.display_name, post.id, pickOp, commentId)
        
    def getRandomSub(self) -> Tuple[Subreddit, str]:
        """
            Returns a random subreddit instance
        """

        sub = None
        rand = random.randint(0, 9)

        # 80% chance of random subreddit
        if rand < 8:
            category = "random"
            sub = self.reddit.random_subreddit(nsfw=self.allowNsfw)
        # 10% chance of r/popular
        elif rand < 9:
            category = "popular"
            sub = self.reddit.subreddit("popular")
        # 10% chance of r/all
        elif rand < 10:
            category = "all"
            sub = self.reddit.subreddit("all")

        if sub is None:
            raise Exception("Sub couldn't be read")

        return sub, category

    def getRandomPost(self, sub: Subreddit, category: str) -> Tuple[Submission, bool]:
        """
            Picks a random post from a given subreddit
        """

        pickOp = False

        # Decide filter
        if category == "all":
            filterByHot = True
            rand = random.randint(0, 4)
            pickOp = (rand == 0)
        elif category == "popular":
            filterByHot = False
        else:
            rand = random.randint(0, 1)
            filterByHot = (rand == 0)

        # Get 10 top posts
        if filterByHot:
            posts = sub.hot(limit=10)
        else:
            posts = sub.new(limit=10)

        # Convert to list
        posts = list(posts)

        # Error checking
        if len(posts) == 0:
            raise Exception("No posts in sub")

        # Pick random
        post = random.choice(posts)

        return post, pickOp

    def getRandomCommenter(self, post: Submission) -> Tuple[Redditor, bool, Optional[str]]:
        """
            Returns a random commenter from a given post

            Defaults to OP when there are no (valid) comments
        """
        comments = []
        for comment in post.comments:
            # Only look for actual comments and the user must not be deleted
            if isinstance(comment, MoreComments) or not comment.author:
                continue
            comments.append(comment)
            if len(comments) >= 20:
                break

        # Default to OP if there are no comments
        if len(comments) == 0:
            isOp = True
            redditor = post.author
            commentId = None
        else:
            isOp = False
            comment: Comment = random.choice(comments)
            redditor = comment.author
            commentId = comment.id

        return redditor, isOp, commentId

    def checkMembership(self, name: str) -> bool:
        """
            Checks if a given redditor is a member of the sub

            TODO: Make the redditors table have a "isMember" column or similar

            For now, this method checks if user is in db
        """
        query = """
            SELECT name FROM redditors WHERE name = %s
        """
        print("WARNING: `checkMembership` doesn't yet do what it's supposed to do")
        return (len(self.db.fetchAll(query, (name,))) > 0)

        # query = """
        #     SELECT isMember FROM redditors WHERE name = %s
        # """
        # fetched = self.db.fetchAll(query, (name,)) 
        # # If no user matched name, then user must be new
        # if len(fetched) >= 0:
        #     if fetched[0][0]:
        #         return True
        # return False


# Testing

from os import environ
from dotenv import load_dotenv

load_dotenv()

reddit = Reddit(client_id=environ["ZOKA_ID"],
                client_secret=environ["ZOKA_TOKEN"],
                username="Zokalyx",
                password=environ["ZOKA_PASS"],
                user_agent="theconfluenceBOT")

# Simple queue functionality
print("--Queue functionality--")
t = RedditorQueue(200, reddit)
for i in range(10):
    t.put_nowait(i)
for i in t.generator():
    print(i)

# Database checks
print("\n--Database checks--")
print(t.checkMembership("Zokalyx"))
print(t.checkMembership("Xylakoz"))

# Random redditor
print("\n--Random redditor--")
print(t.getRedditor().name)

# Cycle
print("\n--Cycle twice--")
t.cycle()
t.cycle()
for i in t.generator():
    print(i.name)

# Test empty queue
print("\n--Empty queue--")
for i in t.generator():
    print(i.name)

# Test fill method
print("\n--Filling--")
t.fill(3)
print(t.qsize())
