setInterval(function() {
    var screenWidth = window.innerWidth;

    var columns = Math.min(Math.floor((screenWidth - (20 * 2)) / (400 + 20)), document.getElementById("grid-container").children.length)

    document.getElementById("grid-container").style.gridTemplateColumns = "auto ".repeat(columns);
    // document.getElementById("grid-container").style.marginRight = (screenWidth - 40 - ((400 + 20) * columns)) / (columns -1) * -1 + "px";
    document.getElementById("grid-container").style.width = columns * 400 + (columns - 1) * 20
}, 0);