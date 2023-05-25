let isDrawing = false;

function setup() {
  let canvas = createCanvas(800, 600);
  canvas.parent('drawing-canvas');
  
  canvas.mousePressed(startDrawing);
  canvas.mouseReleased(stopDrawing);
}

function draw() {
  if (isDrawing) {
    stroke(0);
    strokeWeight(2);
    line(pmouseX, pmouseY, mouseX, mouseY);
  }
}

function startDrawing() {
  isDrawing = true;
}

function stopDrawing() {
  isDrawing = false;
}
