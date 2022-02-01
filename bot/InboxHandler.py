from typing import Tuple
from praw.models import Message
from enum import Enum, auto
import DbHandler

class Action(Enum):
    """
        Enum used for classifying what the received message's intention is
    """

    # Add or remove reminder
    Reminder = auto()
    # Do run, real or debug
    Run = auto()
    # Manage server, like updating flairs or adding members
    Manage = auto()


class InboxHandler:
    """
        Class used for handling all messages in inbox
    """

    def __init__(self):
        """
            Creates an inbox handler
        """
        self.reddit = None
        self.whitelist = None
        self.debuggers = None
        self.db = DbHandler.DbHandler()
        raise NotImplementedError

    def processMessage(self, msg: Message) -> None:
        """
            Recognizes the action of the message
        """
        subject = msg.subject
        body = msg.body
        text = subject.lower() + body.lower()
        author = msg.author.name
        authorId = msg.author.id

        LOGGER.info(f"Received message from {author}: {subject} - {body}")

        # Author in whitelist, probably wants to do a run
        # TODO: Make this also recognize flair and member updates
        if author in self.whitelist:
            self.runAndPost()
        elif author in self.debuggers:
            # Debugger specifically asked to do an "official" run:
            if "official" in text:
                self.runAndPost()
            # Debugger wants to test reminders
            elif "remind" in text:
                self.addReminder(authorId)
            elif "stop" in text:
                self.removeReminder(authorId)
            # Debugger wants to test the run system
            elif "test" in text:
                self.run()
        
        # If author is not in whitelist, probably wants a reminder
        # Check if user is a member
        query = "SELECT member FROM redditors WHERE redditId = %s"
        results = self.db.fetchAll(query, (authorId,))

        # Not a member
        if not results[0][0]:
            return

        if "remind" in text:
            self.addReminder(authorId)
        elif "stop" in text:
            self.addReminder(authorId)
        else:
            # TODO: Handle unrecognized input?
            pass   

    def addReminder(self, redditId: str) -> None:
        """
            Subscribes a member to the automatic reminders

            Membership verification has to be done BEFORE calling this function
        """
        # Check if user is already subscribed
        query = "SELECT reminder FROM redditors WHERE redditId = %s"
        results = self.db.fetchAll(query, (redditId,))

        # Already subscribed
        if results[0][0]:
            # TODO: Handle user already subscribed
            return
        
        query = "UPDATE redditors SET reminder = TRUE WHERE redditID = %s"
        self.db.execute(query, (redditId,))
        redditor = self.reddit.redditor(redditId)
        redditor.message("Subscribed", "You will receive reminders if you haven't posted or commented in The Confluence.\n\nReply with \"stop\" to stop receiving reminders.")

    def removeReminder(self, redditId: str) -> None:
        """
            Removes the subscription of a member to automatic reminders
        """

        # Check if user is already unsubscribed
        query = "SELECT reminder FROM redditors WHERE redditId = %s"
        results = self.db.fetchAll(query, (redditId,))

        # Already unsubscribed
        if not results[0][0]:
            # TODO: Handle user already unsubscribed
            return

        query = "UPDATE redditors SET reminder = FALSE WHERE redditID = %s"
        self.db.execute(query, (redditId,))
        redditor = self.reddit.redditor(redditId)
        redditor.message("Unsubscribed", "You will stop receiving reminders.")

    def run(self) -> Tuple[str, str]:
        """
            Returns the retention, summary and the detailed arrivals and logs the results
        """
        raise NotImplementedError

    def runAndPost(self) -> None:
        """
            Gets the departures and detailed arrivals and posts the results

            TODO: Notify sender
        """

        retention, summary, detailedArrivals = self.run()

        self.reddit.validate_on_submit =True
        profile = self.reddit.subreddit("U_theconfluenceBOT")

        # Remove duplicates and unstick last summary
        for post in profile.new(limit = 10):
            if f"Run {lastRunNumber + 1}" in post.title:
                post.delete()
            elif post.stickied and "summary" in post.title:
                post.mod.sticky(False)

        # Post detailed arrivals
        profile.submit(f"Run {lastRunNumber + 1} detailed arrivals", detailedArrivals)
        profile.submit(f"Run {lastRunNumber + 1} summary - {retention}% retention", summary)


