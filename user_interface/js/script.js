//Variable, in welche die Konfig-Datei geladen wird
let config;

//Variable, die die Anzahl an Scans beinhaltet
let scan_counter;

//Array mit möglichen Animationsklassen
const animation_classes = [
    "cube__animation-xy-360",
    "cube__animation-x-360",
    "cube__animation-y-360",
    "cube__animation-top-y-360"
];

//variable mit dem niedrigsten awattar preis
let lowest_awattar;
/*
    Sobald Seite geladen ist,
    update Funktion ausführen und 
    Scans laden.
*/
$(document).ready(
    async function() { 
        //Läd Konfiguration in globale Variable
        config = getConfig();

        //läd object
        lowest_awattar = await getLowestAwattar();

        // Aktuelle Daten werden in das localStorage geladen
        reloadStorage();

        // Scans von aktuellen Daten werden auf der Seite aufgebaut
        buildSite();

        // Zähle Anzahl Scans auf der Seite
        count_scans();

        // Ständige akualisierung der Seite
        update();
    }
);


/*
    Funktion, um die Seite ständig zu aktualiseren
*/
function update() {
    if(localStorage.getItem("json_data") != JSON.stringify(getData())) {
        // Scans auf der Seite werden gelöscht
        clearSite();

        // Seite wird mit neuen Daten aufgebaut
        buildSite();

        // Aktuelle Daten werden wieder in das localStorage geladen
        reloadStorage();

        // reset scan_counter
        count_scans();

        if(config['general']['debug_mode']) {
            console.log("display new data. reload storage");
        }
    } else {
        if(config['general']['debug_mode']) {
            console.log("data is equal");
        }
    }

    setTimeout('update()', config['general']['page_refresh_rate']);
}


/*
    Funktion um Konfigurationsdatei auszulesen
*/
function getConfig() {
    let request, conf_content;
    request = new XMLHttpRequest();
    request.open("GET","config.json", false);
    request.send(null);
    conf_content = JSON.parse(request.responseText);
    return conf_content;
}

/*
    Funktion die die Scans auf der Seite zählt
*/
function count_scans() {
    let n = 0;
    let scans = getData().scans;
    scans.forEach(scan => {
        n = n + 1;
    });

    scan_counter = n;

    if(config['general']['debug_mode']) {
        console.log("Counted Scans: " + scan_counter);
    }
}

/*
    Funktion die alle Scans auf der Seite darstellt
*/
function buildSite() {
    let lowest = lowest_awattar;
    let lowest_start = lowest.start_timestamp;
    let lowest_end = lowest.end_timestamp;

    const time = new Date(lowest_start).toLocaleTimeString("de-de");
    const date = new Date(lowest_start).toLocaleDateString("de-de");


    document.getElementById("best_time_tomorrow").innerHTML = date + " " + time;

    let scans = getData().scans;
    scans.forEach(scan => {
        buildScan(scan);
    });
}

/*
    Funktion die alle Scans auf der Seite entfernt
*/
function clearSite() {
    let old_scans = document.querySelectorAll(".scan");
    old_scans.forEach(old_scan => {
        old_scan.remove();
    });
}


/*
    Funktion die den Local Storage zurücksetzt
*/
function reloadStorage() {
    localStorage.setItem("json_data", JSON.stringify(getData()));
}


/*
    Funktion, um mittels AJAX request auf die 
    Scan Daten aus der getData.php zuzugreifen.
    Gibt die Daten als JSON zurück.
*/
function getData() {
    let json_data = function () {
        let tmp = null;
        $.ajax({
            'async': false,
            'type': "GET",
            'global': false,
            'dataType': 'json',
            'url': "ajax/getData.php",
            'data': {},
            'success': function (data) {
                tmp = data;
            }
        });
        return tmp;
    }();
    
    return json_data;
}


/*
    Funktion, um ein Scan HTML-Element zusammenzubauen.
    Die Daten werden hierbei von getData() verwendet.
*/
function buildScan(scan_data) {
    /*
        scan_data._id
        scan_data.timestamp
        scan_data.color
        scan_data.temperature
        scan_data.humidty
        scan_data.duration
        scan_data.x
        scan_data.y
    */
    let dateObject = new Date(scan_data.timestamp * 1000)
    let scan_date = dateObject.toLocaleDateString("de-de");
    let scan_time = dateObject.toLocaleTimeString("de-de");

    let scan; // scan - div
    let box_1, box_2, box_3;

    // creates scan
    scan = document.createElement("div");   
    scan.className = "scan";

    //create scan values
    let id = document.createElement("p");
    id.innerHTML = "Nr. " + scan_data._id;
    let date = document.createElement("p");
    date.innerHTML = scan_date;
    let time = document.createElement("p");
    time.innerHTML = scan_time;
    let cube = buildCube(scan_data.color, animation_classes[config['general']['cube_animation']]); //select animation class here !!!
    let humidity = document.createElement("p");
    humidity.innerHTML = "Luftfeuchtigkeit: " + scan_data.humidity + "%";
    let temperature = document.createElement("p");
    temperature.innerHTML = "Temperatur: " + scan_data.temperature + "°";
    let duration = document.createElement("p");
    duration.innerHTML = "Prod. Dauer: " + scan_data.duration + "s";
    let costs = document.createElement("p");
    //costs.innerHTML = "Prod. Kosten: N/A €";
    costs.innerHTML = "Prod. Kosten: " + scan_data.costs + " €";


    //create scan__boxes

    //1
    box_1 = document.createElement("div");
    box_1.className = "scan__box";

    box_1.appendChild(id);
    box_1.appendChild(date);
    box_1.appendChild(time);


    //2
    box_2 = document.createElement("div");
    box_2.className = "scan__box";

    box_2.appendChild(cube);


    //3
    box_3 = document.createElement("div");
    box_3.className = "scan__box";

    box_3.appendChild(humidity);
    box_3.appendChild(temperature);
    box_3.appendChild(duration);
    box_3.appendChild(costs);

    //append boxes to scan
    scan.appendChild(box_1);
    scan.appendChild(box_2);
    scan.appendChild(box_3);

    // appends scan to contaioner
    document.getElementById("scans").appendChild(scan);
}
function buildCube(color, animation_class = null) {
    //create cube values
    let side1;
    side1 = document.createElement("div");
    side1.className = "cube__face cube__face-" + color;
    let side2;
    side2 = document.createElement("div");
    side2.className = "cube__face cube__face-" + color;
    let side3;
    side3 = document.createElement("div");
    side3.className = "cube__face cube__face-" + color;
    let side4;
    side4 = document.createElement("div");
    side4.className = "cube__face cube__face-" + color;
    let side5;
    side5 = document.createElement("div");
    side5.className = "cube__face cube__face-" + color;
    let side6;
    side6 = document.createElement("div");
    side6.className = "cube__face cube__face-" + color;

    let animation;
    animation = document.createElement("div");
    if(animation_class == null) {
        animation_class = "cube__animation-top-y-360";
    }
    animation.className = "cube " + animation_class;

    animation.appendChild(side1);
    animation.appendChild(side2);
    animation.appendChild(side3);
    animation.appendChild(side4);
    animation.appendChild(side5);
    animation.appendChild(side6);

    //create cube
    let cube;
    cube = document.createElement("div");
    cube.className = "cube__scene";

    cube.appendChild(animation);

    return cube;
}

/*
    Funktione, welche eine zufällige Nummer generiert
*/  
function randomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min)
}


/*
    Funktion, die die Liste der Awattar preise als array zurückgibt
*/
async function getLowestAwattar() {
    const url = "https://api.awattar.de/v1/marketdata";
    
    if(config['general']['debug_mode']) {
        console.log(url);
    }
    
    const response = await fetch(url);
    const data = await response.json();

    let temp = 0;
    let lowest = 0;

    for(i = 0; i < data.data["length"]; i++) {
        let marketprice = data.data[i.toString()].marketprice;
        if(temp == 0) {
            temp = marketprice;
        }

        if(marketprice < temp) {
            lowest = data.data[i.toString()];
            temp = marketprice;
        }

    }

    if(config['general']['debug_mode']) {
        console.log(lowest);
    }

    return lowest;
}