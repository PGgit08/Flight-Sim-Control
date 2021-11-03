/**
 * Possible Javascript extension for flight sim.
 * Communicates with geofs.
 * 
 * SOME GEOFS DATA
 * geofs.airplane.instance: get info on current airplane instance
 * controls: control data on current airplane
 */

async function connect(baudrate){
    // get deviced
    const devices = await navigator.serial.getPorts();

    // can't do requestPort for some reason, so hardcoded for now
    console.log("DEVICES FOUND: " + devices);
    console.log("CURRENT DEVICE: " + devices[0]);

    const device = devices[0];
    device.open({baudRate: baudrate})

    return device;
};

connect(9600).then(() => readData());


// function for reading arduino data
async function readData(arduino){
    console.log(arduino);
    // const reader = arduino.readable.getReader(); 

    // while (true){
    //     const {value, done} = await reader.read();

    // };
};
