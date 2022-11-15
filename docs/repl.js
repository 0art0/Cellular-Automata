const canvas = document.getElementById("grid");
const ctx = canvas.getContext("2d");

const screenWidth = canvas.width; const screenHeight = canvas.height;
const blockWidth = 25; const blockHeight = 25;

var play = false; var waitTime = 150;

ctx.strokeStyle = "dimgray";

cellGrid = [];

class Cell {
    constructor(x, y) {
        this.isActive = false;
        this.x = x; this.y = y;
        this.color = "white";
    };

    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.rect(this.x, this.y, blockWidth, blockHeight);
        ctx.stroke(); ctx.fill();
        ctx.closePath();
    };    

    update(activeStatus) {
        this.isActive = activeStatus;
        this.color = activeStatus ? "black" : "white";

        this.draw();
    };

    toggle() {
        this.update(!this.isActive);
    }

    neighbors() {
        return neighborhood(Math.floor(this.x/blockWidth), Math.floor(this.y/blockHeight))
    };

    nextState() {
        var activeNeighborCount = 0;
        var neighborCells = this.neighbors();

        console.log("Cell: " + this.x + ", " + this.y + " ; Neighbours: " + neighborCells)

        for (var i = 0; i < neighborCells.length; i++) { 
            activeNeighborCount += neighborCells[i].isActive
        };

        return (mod(activeNeighborCount, 2) == 1);
    };
};

function initializeGrid() {
    for (var i = 0; i < screenWidth; i += blockWidth) {
        row = [];

        for (var j = 0; j < screenHeight; j += blockHeight) {
            newCell = new Cell(i, j);
            row.push(newCell);
            newCell.draw();
        }

        cellGrid.push(row);
    }
}

function mod(a, n) {
    if ((0 <= a) && (a < n)) {
        return a;
    } else {
        if (a < 0) {
            return mod(a + n, n);
        } else {
            return mod(a - n, n);
        }
    };
}

function neighborhood(i, j) {
    cell = cellGrid[i][j];

    return [
        cellGrid[mod(i-1, cellGrid[i].length)][j], cellGrid[mod(i+1, cellGrid[i].length)][j],
        cellGrid[i][mod(j-1, cellGrid.length)], cellGrid[i][mod(j+1, cellGrid.length)]
    ]
}

function updateBoard() {
    if (play) {
        futureStates = [];

        for (const gridrow of cellGrid) {
            var row = [];
            for (const cell of gridrow) {
                row.push(cell.nextState());
            } 
            futureStates.push(row);
       };

        for (var i = 0; i < cellGrid.length; i++) {
            for (var j = 0; j < cellGrid[i].length; j++) {
                if (((i == 0) || (i == cellGrid.length-1) || (j == 0) || (j == cellGrid[i].length-1)) && (cellGrid[i][j].isActive)) {
                    stopGame();
                    document.getElementById("messagelog").innerHTML = "The cells have reached the edges of the board.";
                }

                cellGrid[i][j].update(futureStates[i][j]);
            }
        }
    }
};

function mouseDraw(evt) {
    var canvasRect = canvas.getBoundingClientRect();
    mx = Math.floor((evt.clientX - canvasRect.left)/blockWidth);
    my = Math.floor((evt.clientY - canvasRect.top)/blockHeight);

    cellGrid[mx][my].toggle();
}

function playPause() {
    play = !play;
    document.getElementById("playpausebutton").innerHTML = play ? "PAUSE" : "PLAY";
}

function stopGame() {
    play = false;
    document.getElementById("playpausebutton").innerHTML = "PLAY";
}

function resetBoard() {
    stopGame();
    document.getElementById("messagelog").innerHTML = "";
   
    for (var i = 0; i < cellGrid.length; i++) {
        for (var j = 0; j < cellGrid[0].length; j++) {
            cellGrid[i][j].update(false);
        }
    }
}

function playGame() {
    initializeGrid();
    canvas.addEventListener("mousedown", mouseDraw);
    
    automaton = setInterval(function () {updateBoard(); }, waitTime);
}

window.onload = playGame();
