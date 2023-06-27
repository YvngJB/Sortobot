<?php
    require 'client.php';

    $conf = [
        'broker' => '212.227.208.209',
        'port' => 1883,
        'topic' => '/robby/mqtt'
    ];

    $mqtt = new Client();
    $mqtt->loadConfig($conf);
    $mqtt->connect();

    $data = $mqtt->subscribe();
    print_r($data);

    $mqtt->disconnect();
?>