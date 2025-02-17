﻿using MQTTnet.Diagnostics;
using System.Diagnostics;

namespace MQTTnet.Client.Extensions;

public class MqttNetTraceLogger
{
    [DebuggerStepThrough()]
    public static MqttNetEventLogger CreateTraceLogger()
    {
        var logger = new MqttNetEventLogger();
        logger.LogMessagePublished += (s, e) =>
        {
            var trace = $">> [{e.LogMessage.ThreadId}]: {e.LogMessage.Message}";
            if (e.LogMessage.Exception != null)
            {
                trace += Environment.NewLine + e.LogMessage.Exception.ToString();
            }

            Trace.TraceInformation(trace);
        };
        return logger;
    }
}
