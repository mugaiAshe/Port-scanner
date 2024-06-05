# Port-scanner
Port scanner with both multi-threaded and single threaded capabilities.

tcpScan：扫描ip地址的一个端口，如果该端口开放tcp连接则记录入open_ports。

scan：创建调用tcpScan的线程，并行扫描一个端口号列表。

main：设置参数，并行ping一个ip地址段，为并行ping和scan计时。
