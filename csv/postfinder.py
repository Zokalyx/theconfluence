import csv
import praw


def insert(ele):
    ind = 0
    for p in data:
        if ele[1] < p[1]:
            break
        else:
            ind += 1
    data.insert(ind, ele)


with open("../graphs/leaderboard/shh.txt", "r") as secret:
    secrets = secret.readlines()
reddit = praw.Reddit(client_id="xskzciRXmoU-JA",
                     client_secret=secrets[1],
                     username="Zokalyx",
                     password=secrets[0].strip(),
                     user_agent="theconfluenceBOT")

pb = []  # List containing all the csv data
pro = open("probyuser.csv", "r", newline="")
with pro:
    reader = list(csv.reader(pro))
    for row in reader[:-200]:
        count = 0
        for el in row[1:]:
            if int(el) != 0:
                count += 1
        if count >= 2:
            index = 0
            for i in range(len(row[1:])):
                if int(row[1:][i]) != 0:
                    index = i
                    break
            pb.append([row[0], index])
    for row in reader[-200:]:
        index = 0
        for i in range(len(row[1:])):
            if int(row[1:][i] != 0):
                index = i
                break
        pb.append([row[0], index])
pro.close()

extra_users = ["theconfluencer", "Or-Your-Money-Back", "EllieTheBeautiful"]
for user in extra_users:
    pb.append([user, 0])

print(len(pb))

# starting = int(input("Select index of user to continue search from: "))
# duration = int(input("Select how many users to process: "))

starting = 0
duration = len(pb)

original = 1583809200
week = 604800

results = [0, 0, 0, 0]  # [Users with no posts, Users with posts, Users with more than 1000 posts (unknown)]
unknown = [[], []]  # third of above.

data = []

for i in range(duration):
    ai = starting + i
    if ai >= len(pb):
        break
    state = 0  # 0 = False, 1 = True, -1 Unknown, Deleted/Badly written user(name)
    print("Index: " + str(ai))
    print("Username: " + pb[ai][0])
    print("Starting search from week: " + str(pb[ai][1] - 1))
    try:
        user = reddit.redditor(pb[ai][0])
        posts = user.submissions.new(limit=None)
        counter = 0
        many = 0
        for post in posts:
            counter += 1
            if post.created_utc < 1583809200 + (pb[ai][1] - 1)*week:
                break
            if post.subreddit.display_name == "TheConfluence":
                insert([post.id, post.created_utc, post.title, post.author.name])
                many += 1
                state = 1
        if counter > 950:
            state = -1
    except:
        state = -2

    if state == -1:
        unknown[0].append(pb[ai][0])
        results[2] += 1
        print("Limit reached")
    elif state == -2:
        unknown[1].append(pb[ai][0])
        results[3] += 1
        print("404")
    else:
        results[state] += 1
        print("Posts found: " + str(many))

    print("\n")

print(data)
print("[no posts, posts, unknown, 404]")
print(results)

proby = open("posts.csv", "w", newline="", encoding="utf-8")  # Write the data
with proby:
    writer = csv.writer(proby)
    for row in data:
        writer.writerow(row)
proby.close()
