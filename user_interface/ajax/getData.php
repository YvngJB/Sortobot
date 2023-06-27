<?php

    use PhpMqtt\Client\Exceptions\MqttClientException;

    # read config file here
    $json_file = file_get_contents("../config.json");
    $config = json_decode($json_file, true);

    /*
        Placeholder for MQTT logic.
        The MQTT server have to transmit the data as json like the
        following data ($json_data);
    */
    require '../model/mqtt/client.php';

    # mqtt client here
    $conf = [
        'broker' => $config['mqtt_connection']['host'],
        'port' => $config['mqtt_connection']['port'],
        'topic' => $config['mqtt_connection']['topic']
    ];

    $mqtt = new Client();
    $mqtt->loadConfig($conf);
    $mqtt->connect();
    try {
        $data = $mqtt->subscribe();
    } catch (MqttClientException $e) {
        $data = null;
    }
    $mqtt->disconnect();

    
    # result of mqtt schould look like this
/*
    $data = 
    [
        'scans' =>
        [
            [
                '_id' => 1,  //int
                'timestamp' => strtotime("2000-01-01 01:01:41"),  //string
                'color' => 'grey', //string
                'temperature' => 0.1,    //float = in grad °
                'humidity' => 40.5,     //float = in prozent %
                'duration' => 54, //float = in sekunden s
            ],
            [
                '_id' => 2,  //int
                'timestamp' => strtotime("2022-06-23 09:04:49"),  //string
                'color' => 'red', //string
                'temperature' => 22.3,    //float = in grad °
                'humidity' => 43.5,     //float = in prozent %
                'duration' => 54, //float = in sekunden s
            ],
            [
                '_id' => 3,  //int
                'timestamp' => strtotime("2022-06-23 09:06:12"),  //string
                'color' => 'blue', //string
                'temperature' => 25.3,    //float = in grad °
                'humidity' => 39.5,     //float = in prozent %
                'duration' => 51, //float = in sekunden s
            ],
            [
                '_id' => 4,  //int
                'timestamp' => strtotime("2022-06-22 12:06:11"),  //string
                'color' => 'green', //string
                'temperature' => 22.7,    //float = in grad °
                'humidity' => 51.1,     //float = in prozent %
                'duration' => 43, //float = in sekunden s
            ],
            [
                '_id' => 5,  //int
                'timestamp' => strtotime("2021-01-12 14:13:11"),  //string
                'color' => 'yellow', //string
                'temperature' => 15.7,    //float = in grad °
                'humidity' => 53.1,     //float = in prozent %
                'duration' => 43, //float = in sekunden s
            ]
        ]
    ];
*/

    echo $data;
?>