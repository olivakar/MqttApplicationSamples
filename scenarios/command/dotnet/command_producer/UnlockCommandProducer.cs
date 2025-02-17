﻿using MQTTnet.Client;
using MQTTnet.Client.Extensions;
using proto_messages;

namespace command_producer;

public class UnlockCommandProducer : CommandProducer<unlockRequest, unlockResponse>
{
    public UnlockCommandProducer(IMqttClient mqttClient)
        : base(mqttClient, "unlock", new ProtobufSerializer(unlockRequest.Parser))
    {
        RequestTopicPattern = "vehicles/{clientId}/command/{commandName}/request";
    }
}
