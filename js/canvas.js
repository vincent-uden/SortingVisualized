var canvas = document.querySelector('canvas');
var c = canvas.getContext('2d');

canvas.width = 1200;
canvas.height = 600;
// Setting up important variables
var sorter = "None";
var types = ["gnome", "selection", "None"];
var colour = 'rgb(242, 160, 63)';
var highlight = 'rgb(255, 31, 0)';
var highlighted = [];
var barArray = [];
var currentIndex = 0;
// Populating barArray
for (var i = 1; i < 60; i++) {
  barArray.push(i * 10);
}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}
// Used in index.hmtl for onlick action
function setSorter(type) {
  sorter = type;
  currentIndex = 0;
}

function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
}

function renderArray(array) {
  c.fillStyle = colour;
  c.clearRect(0, 0, canvas.width, canvas.height);
  var offset = 10;
  for (var i = 0; i < array.length; i++) {
    if (highlighted.includes(i))  {
      c.fillStyle = highlight;
      c.fillRect(offset, 595 - array[i], 15, array[i]);
      offset += 20;
    } else {
      c.fillStyle = colour;
      c.fillRect(offset, 595 - array[i], 15, array[i]);
      offset += 20;
    }
  }
}

function gnomeSort(array) {
  var length = array.length;
    highlighted = [currentIndex, currentIndex - 1]
    if (currentIndex == length) { highlighted = []; setSorter("None"); currentIndex = 0; }
    else if (currentIndex == 0) { currentIndex++; }
    else if (array[currentIndex] < array[currentIndex - 1]) {
      var tmp = array[currentIndex - 1];
      array[currentIndex - 1] = array[currentIndex];
      array[currentIndex] = tmp;
      currentIndex--;
    } else {currentIndex++;}
  return array;
}

var isSelecting = true;
var smallest = 0;
var section = 0;
function sel(arr) {
  highlighted = [currentIndex, smallest];
  if (section == arr.length) {
    setSorter("None");
    isSelecting = true;
    smallest = 0;
    section = 0;
  }
  if (isSelecting) {
    if (currentIndex == arr.length) {
      isSelecting = false;
    } else if (arr[currentIndex] < arr[smallest]) {
      smallest = currentIndex;
    }
    currentIndex++;
  } else {
    var smol = arr[smallest];
    arr.splice(smallest, 1);
    arr.splice(section, 0, smol);
    section++;
    isSelecting = true;
    smallest = section;
    currentIndex = section;
  }
}
// Sorting and rendering "tick"
function update() {
  if (sorter == "gnome") {
    gnomeSort(barArray);
    renderArray(barArray);
  } else if (sorter == "selection") {
    sel(barArray);
    renderArray(barArray);
  }
}
// Request animation, update screen and delay the animation
function animate() {
  window.requestAnimationFrame(animate);
  update();
  sleep(0);
}
// Inital rendering
renderArray(barArray);
animate();
