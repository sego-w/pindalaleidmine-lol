function pencil (){
    canvas.onmousedown = function (e){
        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        hold = true;
             
        prevX = curX;
        prevY = curY;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
    };
         
    canvas.onmousemove = function (e){
        if(hold){
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            draw();
        }
    };
         
    canvas.onmouseup = function (e){
        hold = false;
    };
         
    canvas.onmouseout = function (e){
        hold = false;
    };
         
    function draw (){
        ctx.lineTo(curX, curY);
        ctx.stroke();
        canvas_data.pencil.push({ "startx": prevX, "starty": prevY, "endx": curX, "endy": curY, 
            "thick": ctx.lineWidth, "color": ctx.strokeStyle });
    }
}

function fill (){
    fill_value = true;
    stroke_value = false;
}

function color (color_value){
    ctx.strokeStyle = color_value;
    ctx.fillStyle = color_value;
}

function add_pixel (){
    ctx.lineWidth += 1;
}
         
function reduce_pixel (){
    if (ctx.lineWidth == 2)
        return;
    else
        ctx.lineWidth -= 1;
}

function fill (){
    fill_value = true;
    stroke_value = false;
}
         
function outline (){
    fill_value = false;
    stroke_value = true;
}

function save (){
    var filename = document.getElementById("fname").value;
    var data = JSON.stringify(canvas_data);
     
    $.post("/", { save_fname: filename, save_cdata: data });
    alert(filename + " saved");
     
}
