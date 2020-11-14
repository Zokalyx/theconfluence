var week = 36;

/* LOGIC VARIABLES */
var array; /* Array of all csv data */
var arr; /* Array of the user on screen */
var number; /* Index in variable array of user on screen */
var success = false;
var lastsuccess = false;
var loaded = false;
var specialIndex = 0; /* last week alive (defaults to week when user is still active) */

/* FILTER VARIABLES */
var name = $("#input").val();
var minimumWeeksAllowed = 3;
var validIndices = []; /* List of all indexes of users that passed the filter */

/* RENDER VARIABLES */
var targetvalues = [];
var actualvalues = [];
for (var i = 0; i < week; i++) {
    actualvalues.push(0);
}
var lastvalues = [];
var maximus = 1; /* Maximum flair. Doesn't change when success is false. */
var lastmaximus = 1; /* Last maximus. Defaults to maximus when success if false */
var alphavalue = 0;
var dt = 0.03;
var joining = [];
var leaving = [];
var thisweek = 0; /* Current y value for y axis tick */
var lastweek = 0; /* Last y value for y axis tick */

/* GET CSV DATA AND STORE IT IN VARIABLE ARRAY */
$(document).ready(function() {
    $.ajax({
        method: "GET",
        url: "../csv/probyuser.csv",
        dataType: "text",
        success: function(data) {array = data.split("\n"); loaded = true;}
     });
});

/* CHECK IF NAME IS LIST, UPDATE "ARR" AND "NUMBER" IF SO */
function updateSuccess() {
    lastsuccess = success;
    success = false;
    for (var i = 0; i < array.length-1; i++) {
        if (array[i].split(",")[0].toUpperCase() == name.toUpperCase()) {
            success = true;
            arr = array[i];
            number = i;
            break;
        }
    }
}

/* UPDATES JOINING AND LEAVING ARRAYS */
function updateJoilea() {
    joining = [];
    leaving = [];
    if (success) {
        var last = 0;
        for (var i = 1; i < week+1; i++) {
            if (i != 1) {
                last = parseInt(arr.split(",")[i-1]);
            }
            var actual = Number(arr.split(",")[i]);
            if (actual > last) {
                joining.push([i, actual]);
            }
            if ((actual === 0 || actual > last) && last > 0) {
                leaving.push([i,last]);
            }
        }
    }
}

/* UPDATE THISWEEK AND LASTWEEK */
function updateWeek() {
    lastweek = thisweek;
    if (success) {
        thisweek = parseInt(arr.split(",")[arr.split(",").length-1]);
        specialIndex = week;
        if (thisweek === 0) {
            thisweek = leaving[leaving.length-1][1];
            specialIndex = leaving[leaving.length-1][0];
        }
    } else {
        thisweek = 0;
    }

}

/* RESET ALPHA ONLY IF THERE IS AN ANIMATION TO PLAY */
function resetAlpha() {
    if (!(!lastsuccess && !success)) {
            alphavalue = 0;
        }
        lastvalues = [...actualvalues];
}

/* UPDATE TARGET VALUES AND THAT STUFF AND MAXIMUS */
function updateValues() {
    lastmaximus = maximus;
    if (success) {
        targetvalues = arr.split(",");
        targetvalues.splice(0, 1);
        for (var i = 0; i < week; i++) {
            targetvalues[i] = parseInt(targetvalues[i]);
        }
        maximus = Math.max(...targetvalues);
        for (var i = 0; i < week; i++) {
            targetvalues[i] /= maximus;
        }
        console.log(arr);
    } else {
        for (var i = 0; i < week; i++) {
            targetvalues[i] = 0;
        }
    }
}

/* CHECK IF STRING Y STARTS WITH X */
function sameStart(x, y) {
    var xarray = x.split("");
    var yarray = y.split("");
    var same = true;
    for (var i = 0; i < xarray.length; i++) {
        if (xarray[i] !== yarray[i]) {
            same = false;
            break;
        }
    }
    return same;
}

/* CHECKS IF THE USER HAS CHANGED ANY OF THE FILTERS EXCLUDING NAME */
function filtersChanged() {

}

/* AUX FUNCTION FOR RUNFILTER */
function interchange(a, b) {
    a = [...b];
    b = [];
}

/* CHANGES VALIDINDICES TO WHATEVER MATCHES THE FILTERS */
function runFilter() {
    var auxvalid;
    interchange(auxvalid, validIndices);
    /* BY NAME */
    for (var i = 0; i < array.length; i++) {
        if (sameStart(name.toUpperCase(), array[i].split(",")[0].toUpperCase())) {
            validIndices.push(i);
        }
    }
    /*interchange(auxvalid, validIndices);
    /* BY TIME STAYED */

}

/* GETS CALLED EVERY TIME THERE IS A NEW NAME */
function processData() {
    updateSuccess();
    updateJoilea();
    updateWeek();
    resetAlpha();
    updateValues();
}

function getRandom() {
    var foundIt = false;
    while (!foundIt) {
        number = Math.floor(Math.random() * array.length);
        var auxname = array[number].split(",")[0];
        var numberCount = 0;
        for (var i = 1; i < week+1; i++) {
            if (array[number].split(",")[i] > 0) {
                numberCount++;
                if (numberCount == 3) {
                    foundIt = true;
                    break
                }
            }
        }
    }
    $("#input").val(auxname);
}

/* RETURNS SMOOTH DISTRIBUTION OF POINTS */
function smoothFunc(original, target, percentage) {
    return original + (target-original)*0.5*(1-Math.cos(percentage*Math.PI));
}

/* CREATE CANVAS */
function setup() {
    var canvas = createCanvas(1200,500);
    canvas.parent("canvas");
    background(96);
}

/* UPDATE DRAWING AND LOGIC */
function draw() {
    /* CHECK WHEN THERE IS A NEW NAME */
    if ($("#input").val() !== name && loaded) {
        name = $("#input").val();
        processData();
    }

    /* RENDER GRAPH */
    background(96);
    push();
    translate(width/20, 11*height/16);

        /*BLACK LINES*/
        strokeWeight(1);
        stroke(0);
        line(0, -5/9*height-5, (week-1)/week*9/10*width, -5/9*height-5);
        if (thisweek > 0) {
            var bro = 1;
        } else {
            var bro = 0;
        }
        if (lastweek > 0) {
            var brolast = 1;
        } else {
            var brolast = 0;
        }
        stroke(0,300*smoothFunc(brolast, bro, alphavalue));
        line(0, -5/9*height*smoothFunc(lastweek/lastmaximus, thisweek/maximus, alphavalue)-5,
              (week-1)/week*9/10*width, -5/9*height*smoothFunc(lastweek/lastmaximus, thisweek/maximus, alphavalue)-5);

        /*DRAW POINTS*/
        strokeWeight(9);
        for (var i = 0; i < week; i++) {
            actualvalues[i] = smoothFunc(lastvalues[i], targetvalues[i], alphavalue);
        }
        for (var i = 0; i < week; i++) {
            if (targetvalues[i] > 0) {
                var bro = 1;
            } else {
                var bro = 0;
            }
            if (lastvalues[i] > 0) {
                var brolast = 1;
            } else {
                var brolast = 0;
            }
            stroke(255,0,255,300*smoothFunc(brolast, bro, alphavalue));
            point((i+1)/week*(9/10-1/week)*width, -5/9*height*actualvalues[i]-5);
            for (var j = 0; j < joining.length; j++) {
                if (i + 1 == joining[j][0]) {
                    stroke(255,0,255,300*smoothFunc(brolast, 0, alphavalue));
                }
            }
            if (i > 0 && actualvalues[i-1] !== 0) {
                line((i+1)/week*(9/10-1/week)*width, -5/9*height*actualvalues[i]-5,
                     (i)/week*(9/10-1/week)*width, -5/9*height*actualvalues[i-1]-5);
            }

        }
        if (thisweek > 0) {
            var bro = 1;
        } else {
            var bro = 0;
        }
        if (lastweek > 0) {
            var brolast = 1;
        } else {
            var brolast = 0;
        }
        stroke(255,300*smoothFunc(brolast, bro, alphavalue));
        strokeWeight(5);
        line(-height/50, -5/9*height*smoothFunc(lastweek/lastmaximus, thisweek/maximus, alphavalue)-5,
              height/50, -5/9*height*smoothFunc(lastweek/lastmaximus, thisweek/maximus, alphavalue)-5);
        fill(255,300*smoothFunc(brolast, bro, alphavalue));
        textSize(20);
        strokeWeight(0);
        text(thisweek,-33,-5/9*height*smoothFunc(lastweek/lastmaximus, thisweek/maximus, alphavalue)+1);


        /* MAKE AXES */
        strokeWeight(5);
        stroke(255);

        line(0,0,9*width/10,0);
        line((week-1)/week*9/10*width, height/50, (week-1)/week*9/10*width, -height/50);

        line(0,0,0,-3*height/5);
        line(-height/50, -5/9*height-5, height/50, -5/9*height-5);

        strokeWeight(0);
        fill(255);
        textSize(20);
        text(week,(week-1)/week*9/10*width,30);

        if (thisweek > 0) {
            var bro = 1;
        } else {
            var bro = 0;
        }
        if (lastweek > 0) {
            var brolast = 1;
        } else {
            var brolast = 0;
        }
        fill(255,300*smoothFunc(brolast, bro, alphavalue));
        text(maximus,-33,-5/9*height+1);

        pop();

        /* WRITE NAME */
        if (success) {
            fill(0,255,0);
        } else {
            fill(255,100,100);
        }
        strokeWeight(0);
        textAlign(CENTER);
        textSize(35);
        text(name, width/7+25, 6*height/7);
        textSize(20);
        fill(255);
        for (var i = 0; i < joining.length; i++) {
             if (joining.length == 0) {
                break
             }
             var followingText;
             var previousText = "";
             if (i > 0) {
                previousText = "Re-"
             }
             var plural = "";
             if (leaving.length > i) {
                if (leaving[i][0] - joining[i][0] > 1) {
                    plural = "s"
                }
                followingText = (leaving[i][0] - joining[i][0]) + " week" + plural + " - Left: week " + leaving[i][0] + " (flair: " + leaving[i][1] + ")";
             } else {
                if (week - joining[i][0] > 1) {
                    plural = "s"
                }
                followingText = (week - joining[i][0]) + " week" + plural + " - Currently a member (flair: " + arr.split(",")[arr.split(",").length-1].trim() + ")";
             }
            text(previousText + "Joined: week " + joining[i][0] + " (flair: " + joining[i][1] + ") - Stayed: " + followingText, 4*width/7+75, 6*height/7 - 3 + 30*i);
        }

    /* MANAGE ALPHA AND COPY LAST VALUES IF ANIMATION IS COMPLETE  */
    if (alphavalue < 1) {
        alphavalue += dt;
    } else {
        lastvalues = [...targetvalues];
    }
}