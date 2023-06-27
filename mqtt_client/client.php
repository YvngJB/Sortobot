<?php
require('vendor/autoload.php');

use \PhpMqtt\Client\MqttClient;
use \PhpMqtt\Client\ConnectionSettings;
use PhpMqtt\Client\Exceptions\MqttClientException;
use PhpMqtt\Client\Message;

class Client {
    public bool $DEBUG_MODE = false;
    private array $config = [
        'broker' => 'localhost',
        'port' => 1883,
        'topic' => 'php/mqtt-client'
    ];

    private $server;
    private $port;
    private $topic;
    private $client_id;
    private $username;
    private $password;
    private $clean_session;

    private $connectionSettings;
    private $mqtt;

    private $received_message;

    public function __construct()
    {
        $this->server = $this->config['broker'];
        $this->port = $this->config['port'];
        $this->topic = $this->config['topic'];
        $this->client_id = "php-mqtt-" . rand(10, 100);
        $this->username = null;
        $this->password = null;
        $this->clean_session = false;


        $this->connectionSettings = new ConnectionSettings();
        $this->connectionSettings
            ->setKeepAliveInterval(60)
            ->setLastWillTopic('php/mqtt-client/last_will')
            ->setLastWillMessage('client disconnect')
            ->setLastWillQualityOfService(1);

    }
    public function loadConfig(array $config) : bool 
    {
        if(array_key_exists("broker", $config) && array_key_exists("port", $config) && array_key_exists("topic", $config))
        {
            $this->config = $config;
            $this->__construct();

            return true;
        } else {
            if($this->DEBUG_MODE)
            {
                print("[Error] : Loading new configuration failed: Missing Paraneters. Loaded default configuration.");
            }
            return false;
        }
    }
    public function connect() : bool
    {
        try {
            $this->mqtt = new MqttClient($this->server, $this->port, $this->client_id);

            $this->mqtt->connect($this->connectionSettings, $this->clean_session);
            
            if($this->DEBUG_MODE) {
                printf("Successfully connected to broker.\n");
            }
            return true;
        } catch(MqttClientException $e){
            if($this->DEBUG_MODE) {
                print("[Error] : Connection to broker failed. Please try again.");
            }
            exit();
            return false;
        }

        return false;
    }
    public function disconnect() : bool 
    {
        try {
            $this->mqtt->disconnect();
            return true;
        } catch (MqttClientException $e) {
            print("[Error] : Disconnect failed.");
            return false;
        }
    }
    public function subscribe()
    {
        $test = $this->mqtt->subscribe($this->topic, function($topic, $message) {
            if($this->DEBUG_MODE) {
                printf("data received: [%s]\n", $message);
            }
            $this->mqtt->interrupt();
            $this->received_message = $message;
        }, 0);
        $this->mqtt->loop(true);


        return $this->received_message;
    }
}

?>