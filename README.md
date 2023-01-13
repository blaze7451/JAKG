# JAKG (Japanese Knowledge Graph)
Project on making japanese knowledge graph with rule-based method.
<img src="https://raw.githubusercontent.com/blaze7451/JAKG/main/Image/image002.png"  width="100%" height="50%">
Image from [article](https://theinnovator.news/the-business-case-for-knowledge-graphs/) by Jennifer L. Schenker.
### Introduction
In this little project, I build a little file for people to produce knowledge graph from japanese articles. The detailed introduction of knowledge graph can be seen in the [article](https://medium.com/analytics-vidhya/a-knowledge-graph-implementation-tutorial-for-beginners-3c53e8802377). Basically, the process of making knowledge graphs from articles (or from any data sources like structured datasets and unstructured datasets) can be separated into two steps:
* **Knowledge Extraction:** In this step, people will analyze the dependency relation of each tokens in the text data, extract the entities and relations in the data, and finally preserve them as Subject-Predicate-Object (SPO) triples. This prrocess is where NLP plays a key role in making knowledge graph.
* **Graph Construction:** Storing the SPO triples in a Graph database and visualizing them by tools such as networkx library or neo4j.

### Description of the project


### Future improvement
