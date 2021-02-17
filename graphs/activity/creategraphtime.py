import numpy as np
from pathlib import Path
import csv
import math

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

from datetime import datetime
import praw

with open("../leaderboard/shh.txt", "r") as secret:
    secrets = secret.readlines()

reddit = praw.Reddit(client_id="xskzciRXmoU-JA",
                     client_secret=secrets[1],
                     username="Zokalyx",
                     password=secrets[0].strip(),
                     user_agent="theconfluenceBOT")

posts = []  # List containing all the post data (important = id)
with open("../../csv/posts.csv", "r", encoding="utf-8") as lol:
    reader = csv.reader(lol)
    for row in reader:
        posts.append(row)

totalposts = 0
totalcomments = 0
last_utc = 0
poststime = []
commentstime = []
for i in range(24):
    poststime.append(0)
    commentstime.append(0)
postsday = []
commentsday = []
for i in range(7):
    postsday.append(0)
    commentsday.append(0)

for fake_post in posts:
    post = reddit.submission(fake_post[0])
    tim = round((post.created_utc / 3600) % 24)
    if tim == 24:
        tim = 0
    poststime[tim] += 1

    tim = round((post.created_utc / 86400) % 7)
    tim += 2
    if tim >= 7:
        tim -= 7
    postsday[tim] += 1

    totalposts += 1
    print(totalposts/len(posts)*100)
    print(post.title)

    comments = post.comments
    comments.replace_more(limit=None)
    for comment in comments.list():
        tim = round((comment.created_utc / 3600) % 24)
        if tim == 24:
            tim = 0
        commentstime[tim] += 1

        tim = round((comment.created_utc / 86400) % 7)
        tim += 2
        if tim >= 7:
            tim -= 7
        commentsday[tim] += 1
        totalcomments += 1

    last_utc = post.created_utc
    datto = datetime.utcfromtimestamp(last_utc)

print("Last post:")
print(datto)

print("Times")
print(poststime)
print(commentstime)
for p in range(24):
    if poststime[p] != 0:
        print(str(p) + ":00 = " + str(poststime[p]) + " posts")
    if commentstime[p] != 0:
        print(str(p) + ":00 = " + str(commentstime[p]) + " comments")

print("Days")
print(postsday)
print(commentsday)
for p in range(7):
    if postsday[p] != 0:
        print(str(p) + " day of week = " + str(postsday[p]) + " posts")
    if commentsday[p] != 0:
        print(str(p) + " day of week = " + str(commentsday[p]) + " comments")

for i in range(24):
    poststime[i] /= totalposts
    commentstime[i] /= totalcomments
for i in range(7):
    postsday[i] /= totalposts
    commentsday[i] /= totalcomments

data = [['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00',
         '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'],
        ('Time of posts and comments in GMT (+0:00)', [poststime, commentstime])]

data2 = [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        ('Day of posts and comments in GMT', [postsday, commentsday])]


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, -2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def draw(self, renderer):
            """ Draw. If frame is polygon, make gridlines polygon-shaped """
            if frame == 'polygon':
                gridlines = self.yaxis.get_gridlines()
                for gl in gridlines:
                    gl.get_path()._interpolation_steps = num_vars
            super().draw(renderer)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)


                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


N = len(data[0])
theta = radar_factory(N, frame='polygon')

spoke_labels = data.pop(0)
title, case_data = data[0]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
fig.subplots_adjust(top=0.85, bottom=0.05)

ax.set_rgrids( (0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1), ('', '', '', '', '', '', '', '', '', ''))
ax.set_title(title,  position=(0.5, 1.1), ha='center')

for d in case_data:
    line = ax.plot(theta, d)
    ax.fill(theta, d,  alpha=0.25)
ax.set_varlabels(spoke_labels)

plt.savefig("time.png")

# ------------------

N = len(data2[0])
theta = radar_factory(N, frame='polygon')

spoke_labels = data2.pop(0)
title, case_data = data2[0]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
fig.subplots_adjust(top=0.85, bottom=0.05)

ax.set_rgrids( (0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1), ('', '', '', '', '', '', '', '', '', ''))
ax.set_title(title,  position=(0.5, 1.1), ha='center')

for d in case_data:
    line = ax.plot(theta, d)
    ax.fill(theta, d,  alpha=0.25)
ax.set_varlabels(spoke_labels)

plt.savefig("day.png")