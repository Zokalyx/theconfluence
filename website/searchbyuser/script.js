var population = 0;

/* LOGIC VARIABLES */
var array = []; /* Array of all csv data */
var timemachine = [];
var arr; /* Array of the user on screen */
var number; /* Index in variable array of user on screen */
var success = false;
var lastsuccess = false;
var site_loaded = false;
var specialIndex = 0; /* last week alive (defaults to week when user is still active) */

/* FILTER VARIABLES */
var name = $("#input").val();
var minimumWeeksAllowed = 1;
var chooseFrom = "All";
var maxLowestFlair = population;
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
var weekheight;
var thisjoilea = [0,week]; /* Current x values for x value ticks */
var lastjoilea = [0,week];
var joiwidth;
var leawidth;
var bro; /* Aux */

/* LENGTHS */
var blackLineHeight;
var blackLineWidth;
var axisWidth;
var axisHeight;

/* MISC */
var divisor = 5;
var firstRow = [];
var secondRow = [];

/* GET CSV DATA AND STORE IT IN VARIABLE ARRAY ALSO ADJUST SLIDERS*/
$(document).ready(function() {
    $.ajax({
        method: "GET",
        url: "data/csv/probyuser.csv",
        dataType: "text",
        success: function(data) {
                    var primodialArray = data.split("\n");
                    for (var i = 0; i < primodialArray.length - 1; i++) {
                        array.push([]);
                        var primodialArr = primodialArray[i].split(",");
                        array[i].push(primodialArr[0]);
                        for (var j = 1; j < primodialArr.length; j++) {
                            array[i].push(Number(primodialArr[j]));
                            if (j == primodialArr.length-1) {
                                if (Number(primodialArr[j]) !== 0) {
                                    population++;
                                }
                            }
                        }
                    }
                    $("#flairSlider").attr({
                        "max": population,
                    });
                 }
    });
    $.ajax({
        method: "GET",
        url: "data/csv/timemachine.csv",
        dataType: "text",
        success: function(data) {
                    var primodialArray = data.split("\n");
                    for (var i = 0; i < primodialArray.length - 1; i++) {
                        timemachine.push([]);
                        var primodialArr = primodialArray[i].split(",");
                        for (var j = 0; j < primodialArr.length; j++) {
                            timemachine[i].push(primodialArr[j]);
                        }
                    }
                    site_loaded = true;
                 }
    });
    $("#weekSlider").attr({
        "max": week,
    });
});

/* GET TEXT VERSION OF TIME FOR TIME MACHINE */
function getDate(seconds) {
    let dat = "";
    let err = "";
    if (seconds != 0) {
        time = new Date(seconds * 1000);
        dat = time.getFullYear() + "-" + (time.getMonth() + 1) + "-" + time.getDate();
    } else {
        err = "Not found"
    }
    return [dat, err]
}

/* UPDATE TIME MACHINE */
function updateTimeMachine() {
    let important = timemachine[number];
    if (success) {
        let comres = getDate(Number(important[4]));
        let urlx = "https://www.reddit.com/comments/" + important[5] + "/_/" + important[3];
        $("#oldestcomment").html(comres[0]);
        $("#oldestcomment").attr({
            "href": urlx,
        });
        $("#commenterror").html(comres[1]);

        let posres = getDate(Number(important[2]));
        let urly = "https://www.reddit.com/comments/" + important[1];
        $("#oldestpost").html(posres[0]);
        $("#oldestpost").attr({
            "href": urly,
        });
        $("#posterror").html(posres[1]);
    } else {
        $("#oldestcomment").html("");
        $("#oldestcomment").attr({
            "href": "",
        });
        $("#commenterror").html("");
        $("#oldestpost").html("");
        $("#oldestpost").attr({
            "href": "",
        });
        $("#posterror").html("");
    }
}

/* CHECK IF NAME IS LIST, UPDATE "ARR" AND "NUMBER" IF SO */
function updateSuccess() {
    lastsuccess = success;
    success = false;
    for (var i = 0; i < array.length; i++) {
        if (array[i][0].toUpperCase() == name.toUpperCase()) {
            success = true;
            arr = [...array[i]];
            number = i;
            break;
        }
    }
}

/* UPDATES JOINING AND LEAVING ARRAYS */
function updateJoilea() {
    joining = [];
    leaving = [];
    lastjoilea = [...thisjoilea];
    thisjoilea[1] = week;
    if (success) {
        var last = 0;
        for (var i = 1; i < week+1; i++) {
            if (i != 1) {
                last = arr[i-1];
            }
            var actual = arr[i];
            if (actual > last) {
                joining.push([i, actual]);
            }
            if ((actual === 0 || actual > last) && last > 0) {
                leaving.push([i,last]);
                thisjoilea[1] = i-1;
            }
        }
        thisjoilea[0] = joining[0][0];
        if (leaving.length < joining.length) {
            thisjoilea[1] = week;
        }
    } else {
        thisjoilea[0] = 0;
    }
}

/* UPDATE THISWEEK AND LASTWEEK */
function updateWeek() {
    lastweek = thisweek;
    if (success) {
        thisweek = arr[arr.length-1];
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
        targetvalues = [...arr];
        targetvalues.splice(0, 1);
        for (var i = 0; i < week; i++) {
            targetvalues[i] = targetvalues[i];
        }
        maximus = Math.max(...targetvalues);
        console.log(arr);
        for (var i = 0; i < week; i++) {
            targetvalues[i] /= maximus;
        }
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
    var answer = false;
    if (Number($("#weekSlider").val()) !== minimumWeeksAllowed) {
        answer = true;
        minimumWeeksAllowed = Number($("#weekSlider").val());
        var plural = "";
        if (minimumWeeksAllowed > 1) {
            plural = "s"
        }
        $("#labelForWeekSlider").html("Min. stay = " + minimumWeeksAllowed + " week" + plural);
    }
    if ($("#choose").val() !== chooseFrom) {
        answer = true;
        chooseFrom = $("#choose").val();
    }
    if (Number($("#flairSlider").val()) !== maxLowestFlair) {
        answer = true;
        maxLowestFlair = Number($("#flairSlider").val());
        $("#labelForFlairSlider").html("Max. lowest flair = " + maxLowestFlair);
    }
    return answer;
}

/* FILTERS BY NAME START */
function runNameFilter() {
    var auxvalid;
    auxvalid = [...validIndices];
    validIndices = [];
    /* BY NAME */
    for (var i = 0; i < array.length; i++) {
        if (sameStart(name.toUpperCase(), array[i][0].toUpperCase())) {
            validIndices.push(i);
        }
    }
}

/* CHANGES VALIDINDICES TO WHATEVER MATCHES THE FILTERS */
function runFilter() {
    auxvalid = [...validIndices];
    validIndices = [];
    /* BY TIME STAYED */
    for (var i = 0; i < auxvalid.length; i++) {
        var numberCount = 0;
        for (var j = 1; j < week+1; j++) {
            if (array[auxvalid[i]][j] > 0) {
                numberCount++;
                if (numberCount == minimumWeeksAllowed) {
                    validIndices.push(auxvalid[i]);
                    break;
                }
            }
        }
    }

    /* BY ALL/ACTIVE/INACTIVE */
    if (chooseFrom !== "All") {
        auxvalid = [...validIndices];
        validIndices = [];
        if (chooseFrom === "Active") {
            for (var i = 0; i < auxvalid.length; i++) {
                if (array[auxvalid[i]][week] !== 0) {
                    validIndices.push(auxvalid[i]);
                }
            }
        } else if (chooseFrom === "Inactive") {
            for (var i = 0; i < auxvalid.length; i++) {
                if (array[auxvalid[i]][week] == 0) {
                    validIndices.push(auxvalid[i]);
                }
            }
        }
    }

    /* BY MAXIMUM LOWEST FLAIR */
    if (maxLowestFlair < population) {
        auxvalid = [...validIndices];
        validIndices = [];
        for (var i = 0; i < auxvalid.length; i++) {
            if (Math.min(...array[auxvalid[i]].slice(1).filter(num => num > 0)) <= maxLowestFlair) {
                validIndices.push(auxvalid[i]);
            }
        }
    }
}

/* GETS CALLED EVERY TIME THERE IS A NEW NAME */
function processData() {
    updateSuccess();
    updateJoilea();
    updateWeek();
    resetAlpha();
    updateValues();
}

/* SELECTS A RANDOM USER FROM VALIDINDICES */
function getRandom() {
    name = "";
    runNameFilter();
    runFilter();
    if (validIndices.length > 1) {
        number = findAnother(number, validIndices.length);
        var auxname = array[number][0];
        $("#input").val(auxname);
    } else if ((number !== validIndices[0]) || !success) {
        number = validIndices[0];
        var auxname = array[number][0];
        $("#input").val(auxname);
    }
}

/* GETS A USER THAT IS NOT THE ON SCREEN */
function findAnother(differentThan, maxi) {
    var num;
    while (true) {
        num = Math.floor(Math.random()*maxi);
        if (validIndices[num] !== differentThan) {
            break;
        }
    }
    return validIndices[num];
}

/* RETURNS SMOOTH DISTRIBUTION OF POINTS */
function smoothFunc(original, target, percentage) {

    return original + (target-original)*0.5*(1-Math.cos(percentage*Math.PI));
}

/* AUXILIARY FUNCTION FOR DRAWING */
function biop(last, now) {
    var bro = [0,0];
    if (last > 0) {
        bro[0] = 1;
    }
    if (now > 0) {
        bro[1] = 1;
    }
    return bro;
}

/* WRITE WORD IN TWO COLORS */
function twoColors(word, secondword, x, y) {
    var firstWidth = textWidth(word);
    var word2 = secondword.slice(word.length);
    var totalWidth = firstWidth + textWidth(word2);
    fill(50,200,0);
    text(word, x - totalWidth/2, y);
    fill(200);
    text(word2, x + firstWidth  - totalWidth/2, y);
}

/* WRITE SENTENCE IN TWO COLORS */
function twoSentence(word, sentence, x, y) {
    var totalWidth = 0;
    for (var i = 0; i < sentence.length; i++) {
        totalWidth += textWidth(sentence[i]);
        if (i !== sentence.length-1) {
            totalWidth += textWidth(", ");
        }
    }
    totalWidth = -totalWidth/2;
    var widthCounter = 0;
    for (var i = 0; i < sentence.length; i++) {
        var firstPart = sentence[i].slice(0,word.length+1);
        var secondPart = sentence[i].slice(word.length+1);
        fill(50,200,0);
        text(firstPart, x + widthCounter + totalWidth, y);
        widthCounter += textWidth(firstPart);
        fill(200);
        text(secondPart, x + widthCounter + totalWidth, y);
        widthCounter += textWidth(secondPart);
        if (i !== sentence.length-1) {
            text(", ", x + widthCounter + totalWidth, y);
            widthCounter += textWidth(", ");
        }
    }
}

/* RESIZE CANVAS */
function resizedCanvas() {
    let ans = window.innerHeight*1.75;
    if (ans > window.innerWidth*0.9) {
        ans = window.innerWidth*0.9
    }
    return [ans, 5/12*ans]
}

/* FUNCTION VH */
function vh() {
    return window.innerHeight/100;
}

/* CREATE CANVAS */
function setup() {
    var canvas = createCanvas(resizedCanvas()[0], resizedCanvas()[1]);
    canvas.parent("canvas");
    background(96);

    /* LENGTHS VARIABLES */
    blackLineHeight = -5/9*height;
    blackLineWidth = (week-1)/week*9/10*width;
    axisWidth = 9/10*width;
    axisHeight = -3/5*height;
}

/* UPDATE DRAWING AND LOGIC */
function draw() {
    /* CHECK WHEN THERE IS A NEW NAME */
    if ($("#input").val() !== name && site_loaded) {
        name = $("#input").val();
        processData();
        if (success) {
            name = array[number][0];
            $("#input").val(name);
        }
        runNameFilter();
        runFilter();
    }
    /* RUN THE FILTER IF NAME OR FILTERS HAVE CHANGED */
    if (filtersChanged()) {
        runNameFilter();
        runFilter();
    }
    /* UPDATE ACTUALVALUES */
    for (var i = 0; i < week; i++) {
        actualvalues[i] = smoothFunc(lastvalues[i], targetvalues[i], alphavalue);
    }
    /* RESIZE CANVAS */
    /* UPDATE VARIABLES THAT MOVE */
    weekheight = blackLineHeight*smoothFunc(lastweek/lastmaximus, thisweek/maximus, alphavalue)-5;
    joiwidth = blackLineWidth*smoothFunc(lastjoilea[0], thisjoilea[0], alphavalue)/week;
    leawidth = blackLineWidth*smoothFunc(lastjoilea[1], thisjoilea[1], alphavalue)/week;
    /* UPDATE TIME MACHINE */
    updateTimeMachine();

    /* RENDER GRAPH */
    background(96);
    push();
    translate(width/20, 11*height/16);
    textAlign(CENTER);

        /*BLACK LINES*/
        strokeWeight(1);
        stroke(0);
        line(0, blackLineHeight-5, axisWidth, blackLineHeight-5);
        bro = [...biop(lastweek, thisweek)];
        stroke(0,300*smoothFunc(bro[0], bro[1], alphavalue));
        line(0, weekheight, blackLineWidth*(1+1/week), weekheight);
        /* VERTICAL BLACK LINES */
        bro = [...biop(lastjoilea[0], thisjoilea[0])];
        stroke(0,300*smoothFunc(bro[0], bro[1], alphavalue));
        line(joiwidth, 0, joiwidth, axisHeight);
        bro = [...biop(week-lastjoilea[1], week-thisjoilea[1])];
        if (lastsuccess) { bro[0] = 1; }
        if (success) { bro[1] = 1; }
        stroke(0,300*smoothFunc(bro[0], bro[1], alphavalue));
        line(leawidth, 0, leawidth, axisHeight);

        /* DRAW POINTS AND LINES */
        for (var i = 0; i < week; i++) {
            bro = [...biop(lastvalues[i], targetvalues[i])];
            strokeWeight(8);
            stroke(255,0,255,300*smoothFunc(bro[0], bro[1], alphavalue));
            point((i+1)/week*blackLineWidth, blackLineHeight*actualvalues[i]-5);
            for (var j = 0; j < joining.length; j++) {
                if (i + 1 == joining[j][0]) {
                    stroke(255,0,255,300*smoothFunc(bro[0], 0, alphavalue));
                }
            }
            strokeWeight(9);
            if (i > 0 && actualvalues[i-1] !== 0) {
                line((i+1)/week*blackLineWidth, blackLineHeight*actualvalues[i]-5,
                     (i)/week*blackLineWidth, blackLineHeight*actualvalues[i-1]-5);
            }

        }

        /* MOVING TICK MARKS */
        strokeWeight(5);
        bro = [...biop(lastweek, thisweek)];
        stroke(255,300*smoothFunc(bro[0], bro[1], alphavalue));
        line(-height/50, weekheight, height/50, weekheight);
        fill(255,300*smoothFunc(bro[0], bro[1], alphavalue));
        textSize(20);
        strokeWeight(0);
        text(thisweek,-33,weekheight+5);
        /* VERTICAL */
        strokeWeight(5);
        bro = [...biop(lastjoilea[0], thisjoilea[0])];
        stroke(255,300*smoothFunc(bro[0], bro[1], alphavalue));
        line(joiwidth, height/50, joiwidth, -height/50);
        fill(255,300*smoothFunc(bro[0], bro[1], alphavalue));
        strokeWeight(0);
        text(thisjoilea[0],joiwidth,30);

        strokeWeight(5);
        bro = [...biop(week-lastjoilea[1], week-thisjoilea[1])];
        if (lastsuccess) { bro[0] = 1; }
        if (success) { bro[1] = 1; }
        stroke(255,300*smoothFunc(bro[0], bro[1], alphavalue));
        line(leawidth, height/50, leawidth, -height/50);
        fill(255,300*smoothFunc(bro[0], bro[1], alphavalue));
        strokeWeight(0);
        text(thisjoilea[1],leawidth,30);


        /* MAKE AXES */
        strokeWeight(5);
        stroke(255);

        line(0,0,axisWidth,0);
        line(blackLineWidth, height/50, blackLineWidth, -height/50);

        line(0,0,0,axisHeight);
        line(-height/50, blackLineHeight-5, height/50, blackLineHeight-5);

        strokeWeight(0);
        fill(255);
        textSize(20);
        text(week,blackLineWidth,30);

        fill(255,300*smoothFunc(bro[0], bro[1], alphavalue));
        text(maximus,-33,blackLineHeight+1);

    pop();

    /* WRITE NAME */
    strokeWeight(0);
    textSize(40);
    textAlign(CENTER);
    if (success) {
        fill(0,255,0);
        text(name, width/7+25, 6*height/7);
    } else if (validIndices.length == 1) {
        textAlign(LEFT);
        twoColors(name, array[validIndices[0]][0], width/7+25, 6*height/7)
        textAlign(CENTER);
    } else if (validIndices.length == 0) {
        fill(255,100,100);
        text(name, width/7+25, 6*height/7);
    } else {
        fill(50,200,50);
        text(name, width/7+25, 6*height/7);
    }

    textSize(20);
    fill(200);
    /* WRITE INDICATION TO PRESS ENTER */
    if (!success && validIndices.length == 1) {
        text("Press enter to autocomplete", 4*width/7+75, 6*height/7 - 3);
    }

    /* WRITE WARNING */
    if (validIndices.length == 0 && !success) {
        text("No users match both that name and those filters", 4*width/7+75, 6*height/7 - 3);
    }

    /* WRITE SUGGESTIONS */
    if (!success && validIndices.length > 1) {
        textAlign(LEFT);
        firstRow = [];
        secondRow = [];
        for (var i = 0; i < validIndices.length; i++) {
            if (i == divisor) {
                break;
            }
            firstRow.push(" "+array[validIndices[i]][0]);
        }
        twoSentence(name, firstRow, 4*width/7+75, 6*height/7 - 3);
        if (validIndices.length > divisor) {
            for (var i = divisor; i < validIndices.length; i++) {
            if (i == divisor*2) {
                break;
            }
            secondRow.push(" "+array[validIndices[i]][0]);
            }
            twoSentence(name, secondRow, 4*width/7+75, 6*height/7 - 3 - 25);
        }
        textAlign(CENTER);
        if (validIndices.length > divisor*2) {
            text("(and " + (validIndices.length - 2*divisor + " more)"), 4*width/7+75, 6*height/7 - 3 + 25);
        }
    }

    /* WRITE DATA */
    if (success) {
        fill(255);
        for (var i = 0; i < joining.length; i++) {
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
                if (week - joining[i][0] > 0) {
                    plural = "s"
                }
                followingText = (week+1 - joining[i][0]) + " week" + plural + " - Currently a member (flair: " + arr[arr.length-1] + ")";
             }
            text(previousText + "Joined: week " + joining[i][0] + " (flair: " + joining[i][1] + ") - Stayed: " + followingText, 4*width/7+75, 6*height/7 - 3 + 25*i);
        }
    }

    /* MANAGE ALPHA AND COPY LAST VALUES IF ANIMATION IS COMPLETE  */
    if (alphavalue < 1) {
        alphavalue += dt;
    } else {
        lastvalues = [...targetvalues];
    }
}

/* HANDLE ENTER */
function keyPressed() {
    if (keyCode === ENTER) {
        if (validIndices.length === 1 && !success) {
            name = "";
            $("#input").val(array[validIndices[0]][0]);
        }
    }
}