var week = 47;
let wkch, rnch, dtch;
$(document).ready(function() {
    $("#week_place").attr({
       "max" : week
    });
    $("#info_week").html(week)
    $("#info_run").html(week-4)
    $("#run_place").attr({
       "max" : week - 4
    });
});

let texts = ["#week_place", "#run_place", "#date_place"];
let change = false;
let who = -1;

let original = 1583712000000;
let originalprior = 1583722800000;

function weekToMs(week) {
    let ans = originalprior + (week-1)*604800000;
    if (week >= 36) {
        ans += 172800000;
    }
    return ans
}
function msToWeek(ms) {
    let ans;
    let aux = ms - original;
    if (ms >= 1605063600000) {
        aux -= 172800000;
    }
    ans = Math.floor(aux / 604800000) + 1;
    return ans
}
function msToDate(ms) {
    let date = new Date(ms);
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    if (month.toString().length == 1) {
        month = "0" + month;
    }
    let day = date.getDate();
    if (day.toString().length == 1) {
        day = "0" + day;
    }
    return year + "-" + month + "-" + day;
}
function dateToMs(date) {
    let dt = new Date(date);
    return dt.getTime();
}


function weekToRun(week) {
    let ans;
    if (week < 6) {
        ans = week;
    } else if (week < 12) {
        ans = week - 1;
    } else if (week < 36) {
        ans = week - 2;
    } else if (week < 42) {
        ans = week - 3;
    } else {
        ans = week - 4;
    }
    return ans;
}
function runToWeek(run) {
    let ans;
    if (run < 6) {
        ans = run;
    } else if (run < 11) {
        ans = run - (-1);
    } else if (run < 34) {
        ans = run - (-2);
    } else if (run < 39) {
        ans = run - (-3);
    } else {
        ans = run - (-4);
    }
    return ans;
}
function weekToDate(week) {
    return msToDate(weekToMs(week))
}
function dateToWeek(date) {
    return msToWeek(dateToMs(date))
}
function runToDate(run) {
    return weekToDate(runToWeek(run))
}
function dateToRun(date) {
    return weekToRun(dateToWeek(date))
}

function convert(from, to) {
    let fromVal = $(texts[from]).val();
    // console.log(fromVal);
    if (from == 0) {
        if (to == 1) {
            return weekToRun(fromVal);
        }
        if (to == 2) {
            return weekToDate(fromVal);
        }
    } else if (from == 1) {
        if (to == 0) {
            return runToWeek(fromVal);
        } else if (to == 2) {
            return runToDate(fromVal);
        }
    } else if (from == 2) {
        if (to == 0) {
            return dateToWeek(fromVal);
        } else if (to == 1) {
            return dateToRun(fromVal);
        }
    }
}
function checkChange() {
    change = false;
    for (let i = 0; i < 3; i++) {
        if (immune[i]) {
            immune[i] = false;
        } else {
            if (last[i] != $(texts[i]).val()) {
                who = i;
                change = true;
                changes[i] = true;
                for (let j = 0; j < 3; j++) {
                    if (j == i) {
                        continue;
                    }
                    immune[j] = true;
                    // console.log(j);
                }
                last[i] = $(texts[i]).val();
                break;
            } else {
                changes[i] = false;
            }
        }
        last[i] = $(texts[i]).val();
    }
}

last = [false, false, false]
changes = [false, false, false]
immune = [false, false, false]

function draw() {
    checkChange();
    if (change) {
        for (let i = 0; i < 3; i++) {
            if (i == who) {
                continue;
            }
            $(texts[i]).val(convert(who, i));
        }
    }
}

function mouseClicked() {
    //console.log("Changes: " + changes);
    //console.log("Immunities: " + immune);
    //console.log("Last values: " + last);
}