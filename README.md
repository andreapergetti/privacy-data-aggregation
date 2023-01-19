# privacy-data-aggregation

This is an unofficial implementation of a Privacy-Preserving Aggregation of Time-Series Data, as described in the paper 
http://elaineshi.com/docs/ndss2011.pdf. 

The aim of this project is to develop a protocol in which an untrusted data aggregator can learn desired statistics over multiple
participants’ data, without compromising each individual’s privacy. The idea is that there is a group of 
participants that periodically upload encrypted values to a data aggregator, such that the aggregator is able 
to compute the sum of all participants’ values in every time period, but is unable to learn anything else. 
The main properties of this protocol are: <br>
- The scheme is aggregator oblivious, that is aggregator unable to learn anything other than auxiliary knowledge and desired statistics
- Guarantees distributed differential privacy, that statistics revealed will not be swayed too much by whether or not a specific individual participates

You can find further details on the project such as the motivation of the implementation choices, results, complexity, 
execution time and testing in the [documentation](documentation.pdf) file.
