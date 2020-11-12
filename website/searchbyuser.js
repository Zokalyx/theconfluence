var week = 36;
var array;
var loaded = false;

$(document).ready(function() {
    $.ajax({
        method: "GET",
        url: "../csv/probyuser.csv",
        dataType: "text",
        success: function(data) {array = data.split("\n"); loaded = true;}
     });
});

var arr;
var number;
var name = $("#input").val();
var success = false;
var targetvalues = [];
var actualvalues = [];
for (var i = 0; i < week; i++) {
    actualvalues.push(0);
}
var lastvalues = [];
var maximus = "";
var alphavalue = 0;
var dt = 0.03;
var lastsuccess = false;
var joining = [];
var leaving = [];
var thisweek = 0;
var lastweek = 0;
var specialIndex = 0;
var validmaximus = 1;

function processData(name) {
    var row;
    success = false;
    for (var i = 0; i < array.length-1; i++) {
        if (array[i].split(",")[0].toUpperCase() == name.toUpperCase()) {
            row = i;
            success = true;
            break;
        }
    }
    arr = array[row];
    number = row;

    var tojoining = [];
    var toleaving = [];
    var last = 0;
    if (maximus === "") {
        lastweek = 0;
    } else {
        lastweek = thisweek/parseInt(maximus);
    }
    if (success) {
        for (var i = 1; i < week+1; i++) {
            if (i != 1) {
                last = parseInt(arr.split(",")[i-1]);
            }
            if (parseInt(arr.split(",")[i]) > last) {
                tojoining.push([i, parseInt(arr.split(",")[i])]);
            }
            if ((parseInt(arr.split(",")[i]) === 0 || parseInt(arr.split(",")[i]) > last) && last > 0) {
                toleaving.push([i,last]);
            }
        }
        thisweek = parseInt(arr.split(",")[arr.split(",").length-1]);
        specialIndex = week;
        if (thisweek === 0) {
            thisweek = toleaving[toleaving.length-1][1];
            specialIndex = toleaving[toleaving.length-1][0];
        }
    } else {
        thisweek = 0;
    }
    joining = [...tojoining];
    leaving = [...toleaving];
}

function getRandom() {
    var foundIt = false;
    while (!foundIt) {
        number = Math.floor(Math.random() * array.length);
        name = array[number].split(",")[0];
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
    updateAccordingly();
    $("#input").val(name);
}

function updateAccordingly() {
        lastsuccess = success;
        processData(name);
        if (!(!lastsuccess && !success)) {
            alphavalue = 0;
        }
        lastvalues = [...actualvalues];

        /* UPDATE ACCORDINGLY TARGET AND MAXIMUS */
        if (success) {
            values = arr.split(",");
            targetvalues = [...values];
            targetvalues.splice(0, 1);
            for (var i = 0; i < week; i++) {
                targetvalues[i] = parseInt(targetvalues[i]);
            }
            maximus = String(Math.max(...targetvalues));
            for (var i = 0; i < week; i++) {
                targetvalues[i] = targetvalues[i]/maximus;
            }
            validmaximus = parseInt(maximus);
            console.log(arr);
        } else {
            for (var i = 0; i < week; i++) {
                targetvalues[i] = 0;
            }
            maximus = "";
        }
}

function setup() {
    var canvas = createCanvas(1200,500);
    canvas.parent("canvas");
    background(96);
    var values;
}

function smoothFunc(original, target, percentage) {
    return original + (target-original)*0.5*(1-Math.cos(percentage*Math.PI));
}

function draw() {
    /* CHECK WHEN THERE IS A NEW NAME */
    if ($("#input").val() !== name && loaded) {
        name = $("#input").val();
        updateAccordingly();
    }

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
    line(0, -5/9*height*smoothFunc(lastweek, thisweek/validmaximus, alphavalue)-5,
          (week-1)/week*9/10*width, -5/9*height*smoothFunc(lastweek, thisweek/validmaximus, alphavalue)-5);

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
    line(-height/50, -5/9*height*smoothFunc(lastweek, thisweek/validmaximus, alphavalue)-5,
          height/50, -5/9*height*smoothFunc(lastweek, thisweek/validmaximus, alphavalue)-5);
    fill(255,300*smoothFunc(brolast, bro, alphavalue));
    textSize(20);
    strokeWeight(0);
    text(thisweek,-33,-5/9*height*smoothFunc(lastweek, thisweek/validmaximus, alphavalue)+1);


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
    text(validmaximus,-33,-5/9*height+1);


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
            followingText = (week - joining[i][0]) + " week" + plural + " - Currently a member (flair: " + arr.split(",")[arr.split(",").length-1].split("").pop() + ")";
         }
        text(previousText + "Joined: week " + joining[i][0] + " (flair: " + joining[i][1] + ") - Stayed: " + followingText, 4*width/7+75, 6*height/7 - 3 + 30*i);
    }

    /* MANAGE ALPHA */
    if (alphavalue < 1) {
        alphavalue += dt;
    } else {
        lastvalues = [...targetvalues];
    }
}