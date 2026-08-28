# Atlas Edge Agent

The edge agent is reserved for the second phase. It will collect industrial data from PLCs, sensors and machines, buffer locally when offline, and synchronize with Atlas Pulse through MQTT or future transports.

```text
PLC / Sensor / Machine
          |
       Gateway
          |
    Atlas Edge Agent
          |
         MQTT
          |
      Atlas Pulse
```

Planned capabilities: Modbus TCP, Modbus RTU, OPC-UA, Serial, GPIO, local buffering and cloud synchronization.
