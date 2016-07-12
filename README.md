# Reader-Sender

This application implements a reader-sender model. The idea is that a reader reads in a value from a source and a sender sends it to some service.

I typically use this module to create a simulated device (with randomreader) and use it to send data with regular time intervals to a MQTT server.

The class model simplifies creating new senders and readers.
