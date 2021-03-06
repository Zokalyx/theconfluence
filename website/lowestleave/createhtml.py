import csv

week = int(open("../../data/week.txt", "r").readline())  # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])

text = ""
for i in range(week - 1, 0, -1):
    with open("../../data/departures/{}.txt".format(i+1), "r") as dep:
        file = dep.readlines()
        arr = [i for i in file if i != "\n"]
        arr = [i.replace("\n", "") for i in arr]
        arr = [i.replace(".", "") for i in arr]
        if len(arr) == 0:
            continue
        else:
            wk = i + 1
            if wk < 6:
                off = 0
            elif wk < 12:
                off = 1
            elif wk < 36:
                off = 2
            elif wk < 42:
                off = 3
            else:
                off = 4
            run = wk - off
            text += "<h2>Run {}</h2> \n <p class='important'> {} <br> {} <br> {} </p> \n"\
                .format(run, arr[0], arr[1], arr[2])


before = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <base href="https://zokalyx.github.io/theconfluence/">

    <!-- tab -->
    <title>Departures analysis</title>
    <link rel="shortcut icon" type="image/ico" href="website/images/favicon.ico"/>

    <!-- external files -->
    <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="website/script.js"></script>
    <link rel="stylesheet" href="website/style.css">
</head>
<body onload="loaded()">
    <div id="wrapper">
    <!-- header -->
    <header>
        <a href="https://zokalyx.github.io/theconfluence">
            <img id="home" src="">
        </a>
        <a id="github" href="https://github.com/Zokalyx/theconfluence">
            <img class="external" src="website/images/github.png">
        </a>
        <a href="https://discord.gg/K2ykw9K">
            <img class="external" src="website/images/discord.png">
        </a>
        <a href="https://www.reddit.com/r/TheConfluence">
            <img class="external" src="website/images/reddit.png">
        </a>
        <span id="days">
        </span>
    </header>

    <!-- main -->
    <h1>
        Average and lowest flair number of departing people
    </h1>
    <img class="smallcontent" src="website/lowestleave/graph1.png">
    <img class="smallcontent" src="website/lowestleave/graph2.png">
    
     <section class="content">
        <span> Notes </span>
        <p>
            These graphs tries to display the distribution of those who are leaving. The first one uses normal flair
            numbers and the second one uses a percentage of the total (for example, a user with flair 50 would be on
            the 25th percentile if there are 200 people in total).
            <br>
            <br>
            The orange line represents the lowest flair number in any given set of departures. 
            <br>
            Below you can see who these users are as well as the second and third ones for each run.
        </p>
    </section>
    
    <h1>
        Most notable departures
    </h1>
    
"""

after = """

    </div>
    <!-- footer -->
    <footer>
        <div id="container">
            <img id="shh" src="website/images/shh.png">
            <p id="secret">
                This is a private community, so keep this a secret ;) <br>
                Website design and content by u/Zokalyx
            </p>
        </div>
    </footer>
</body>
</html>"""

with open("index.html", "w") as html:
    html.write(before)
    html.write(text)
    html.write(after)
    pass

