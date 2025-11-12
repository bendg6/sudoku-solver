
function scrollButton() {
    document.getElementById("spinner").style.display = "block"
}
function scrollToSection(event, targetId) {
    event.preventDefault();
    const targetElement = document.getElementById(targetId);
    targetElement.scrollIntoView();
    
}
function spinner(){
    document.getElementById('spinner').style.display = 'block';
}
function backgroundColor() {
    if(window.location.href.includes("/solver")) {
        document.body.style.backgroundColor = "#51cba4";
        document.getElementById('solverlink').style.color = "#51cba4";
        document.getElementById('solverlink').style.borderBottom = "2px #51cba4 solid";
        
        }
    if(window.location.href.includes("/methods")) {
        document.getElementById('methodlink').style.color = "#6ea3df";
        document.getElementById('methodlink').style.borderBottom = "2px #6ea3df solid";
        
        }
    if(window.location.href.includes("/puzzles")) {
        document.body.style.backgroundColor = "#eee089";
        document.getElementById('puzzlelink').style.color = "#eee089";
        document.getElementById('puzzlelink').style.borderBottom = "2px #eee089 solid";
        
        }
    if(window.location.href.includes("/home")) {
        document.body.style.backgroundImage = "url('/static/numbers.png')";
        }
        if(window.location.href.includes("/traveleriq")) {
            document.body.style.backgroundColor = "#51cba4";
            }
        }
function switchPics() {
    if(document.getElementById("puzzles").style.display == "block") {
        document.getElementById("puzzles").style.display = "none"
        document.getElementById("dot3").style.opacity = "0.4"
        document.getElementById("dot1").style.opacity = "1"
        document.getElementById("sudokusolver").style.display = "block"
    }
    else{
        if(document.getElementById("sudokusolver").style.display == "block") {
            document.getElementById("sudokusolver").style.display = "none"
            document.getElementById("dot1").style.opacity = "0.4"
            document.getElementById("dot2").style.opacity = "1"
            document.getElementById("methods").style.display = "block"
        }
        else{
        if(document.getElementById("methods").style.display == "block") {
            document.getElementById("methods").style.display = "none"
            document.getElementById("dot2").style.opacity = "0.4"
            document.getElementById("dot3").style.opacity = "1"
            document.getElementById("puzzles").style.display = "block"
        }
        }
    }   
}
function switchMethods() {
    a = "d11";
    b = "d1";
    g = 0
    if(document.getElementById("12").style.display == "block") {
        document.getElementById("12").style.display = "none"
        document.getElementById("1").style.display = "block"
        document.getElementById("d12").style.opacity = 0.4
        document.getElementById("d1").style.opacity = 1
        g = 1
    }
    if(g == 0) {
    for(let i=1; i < 12; i++) {
        a = "d" + i.toString();
        b = "d" + (i+1).toString();
        if(document.getElementById(i.toString()).style.display == "block") {
            document.getElementById(i.toString()).style.display = "none"
            document.getElementById((i+1).toString()).style.display = "block"
            document.getElementById(a).style.opacity = 0.4
            document.getElementById(b).style.opacity = 1
            i = 12
        }
    }
}
}
function changeValue(reds, blues, grays, nums) {
    const letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    for (let i=0; i < 81; i++){
        if(reds.includes(i)){
        document.getElementById(letters[Math.floor(i/9)] + toString(i%9 + 1)).style.color = "red"
        document.getElementById(letters[Math.floor(i/9)] + toString(i%9 + 1)).style.value = nums[i]

        }
        if(blues.includes(i)){
            document.getElementById(letters[Math.floor(i/9)] + toString(i%9 + 1)).style.color = "blue"
            document.getElementById(letters[Math.floor(i/9)] + toString(i%9 + 1)).style.value = nums[i]
    
            }
            if(grays.includes(i)){
                document.getElementById(letters[Math.floor(i/9)] + toString(i%9 + 1)).style.color = "gray"
                document.getElementById(letters[Math.floor(i/9)] + toString(i%9 + 1)).style.value = nums[i]
        
                }
    }

}
function collapsible() {
    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
        content.style.display = "none";
        } else {
        content.style.display = "block";
        }
    });
    }
}
function whiteScreen(){
    document.getElementById('whitescreen').style.display = 'flex'
}
function finishScreen(){
    document.getElementById('finishscreen').style.display = 'none'
}
function clearGrid(){
    var cells = document.getElementsByClassName('searchbar')
    for(let i=0; i < cells.length; i++){
        cells[i].value = ''
    }
}