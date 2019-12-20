//host = 'mqtt://mqtt.eclipse.org'
//host = 'mqtt://mqtt.eclipse.org/mqtt'  // using web socket
//host = 'ws://localhost:1885'

scale = 10
perimeter_pill = 3
perimeter_snakebody = 5
topic = 'mmsnake/world'
mqtt_options = {
    host: 'localhost',
    port: 1885,
    username: 'viewer',
    password: 'viewer'
}
offset = perimeter_pill + 2  // offset in x-/y-direction

// https://entwickler.de/online/javascript/mqtt-mit-javascript-579860931.html

var c = document.getElementById('mmsnake_canvas')
var ctx = c.getContext('2d')
c.width = 800 // document.body.clientWidth
c.height = 800 // document.body.clientHeight

console.log('connecting to %o', mqtt_options)
var client  = mqtt.connect(mqtt_options)

client.on('connect', function() {
    console.log('subscribing to ' + topic)
    client.subscribe(topic)
})

client.on('message', function(topic, message) {
    drawWorld(JSON.parse(message.toString()))
})

function drawWorld(world) {
    ctx.fillStyle = '#FFFFFF'
    ctx.fillRect(0, 0, c.width, c.height)    
    drawPills(world['pills'])
    drawSnakes(world['snakes'])
}

function drawPills(pills) {
    for(pill of pills) {
        x = pill[0]
        y = pill[1]
        drawCircle(x, y, perimeter_pill, '#0000FF', filled=false)
    }
}

function drawCircle(x, y, perimeter, color, filled=false) {
    ctx.beginPath()
    //                                  startangle, end angle
    ctx.fillStyle = color
    ctx.arc(scale*x+offset, scale*y+offset, perimeter, 0, 2 * Math.PI)
    if(filled) {
        ctx.fill()
    } else {
        ctx.stroke()
    }
}

function drawSnakes(snakes) {
    for (snake in snakes) {
        for(bodypart of snakes[snake]['body']) {
            x = bodypart[0]
            y = bodypart[1]
            col = "#" + intToRGB(hashCode(snake))
            drawCircle(x, y, perimeter_snakebody, col, filled=true)
        }
    }
}

// from https://stackoverflow.com/questions/3426404/create-a-hexadecimal-colour-based-on-a-string-with-javascript
function hashCode(str) {
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
       hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
} 

function intToRGB(i){
    var c = (i & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
}
