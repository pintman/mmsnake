//host = 'mqtt://mqtt.eclipse.org'
//host = 'mqtt://mqtt.eclipse.org/mqtt'  // using web socket
//host = 'ws://localhost:1885'

scale = 20
perimeter_pill = 2
perimeter_snakebody = 5
width =  500
height = 500
topic = 'mmsnake/world'
mqtt_options = {
    host: 'localhost',
    port: 1885,
    username: '1',
    password: '123456'
}

// https://entwickler.de/online/javascript/mqtt-mit-javascript-579860931.html

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
    ctx.fillRect(0, 0, width, height)    
    ctx.fillStyle = '#0000FF'
    drawPills(world['pills'])
    drawSnakes(world['snakes'])
}

function drawPills(pills) {
    for(pill of pills) {
        x = pill[0]
        y = pill[1]
        drawCircle(x, y, perimeter_pill)
    }
}

function drawCircle(x, y, perimeter) {
    ctx.beginPath()
    //                                  startangle, end angle
    ctx.arc(scale*x, scale*y, perimeter, 0, 2 * Math.PI)
    ctx.stroke()
}

function drawSnakes(snakes) {
    for (snake in snakes) {
        for(bodypart of snakes[snake]['body']) {
            x = bodypart[0]
            y = bodypart[1]
            drawCircle(x, y, perimeter_snakebody)
        }
    }
}


var c = document.getElementById('canv')
var ctx = c.getContext('2d')
