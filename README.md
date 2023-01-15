# privacy-data-aggregation

The aim of this project is to develop a protocol in which an untrusted data aggregator can learn desired statistics over multiple
participants’ data, without compromising each individual’s privacy. The idea is that there is a group of 
participants that periodically upload encrypted values to a data aggregator, such that the aggregator is able 
to compute the sum of all participants’ values in every time period, but is unable to learn anything else. 
The properties of this protocol are: the scheme is aggregator oblivious (that is aggregator unable to learn 
anything other than auxiliary knowledge and desired statistics) and guarantees distributed differential privacy
(that statistics revealed will not be swayed too much by whether or not a specific individual participates).
