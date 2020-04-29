# Reader-Sender

The readersender package implements a simple reader-sender model, which allows a reader reads to a value from a source and a sender sends it to a target.

The package is built on a class hierarchy, which start from a few abstract base classes, that define the basic interfaces. A few implementation of the class are provided mostly as examples on the ways in which to implement the functionalities.

Class hierarchy
---------------

* ReaderSender

  * Reader(ReaderSender)

  	* FooReader(Reader)

  	* RandomReader(Reader)

  * Sender(ReaderSender)

  	* FooSender(Sender)

  	* MQTTSender(Sender)

  	* IOTFSender(Sender)

  	* IOTFDeviceSender(Sender)