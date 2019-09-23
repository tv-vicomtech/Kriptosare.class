# Kryptosare Analytics

Kryptosare analytics is a tool based on concept of "Cascading Machine Learning" that allows detect entity behaviour related with a certain Bitcoin address. In particular it can distinguish into 6 classes: Exchange, Service, Mixer, Market, Pool and Gambling.
Cascading machine learning approach requires only a few features directly extracted from Bitcoin blockchain data. Cascading, used to enrich entities information with data from previous classifications, led to considerably improved multi-class classification performance.

## Getting Started
### Clone the project
```
git clone git@gitlab.vicomtech.es:TITANIUM_EU9256_2016/TITANIUM-Testbed.git
```

### Cassandra Table
Install Cassandra Database and create the database and tables by executing:

```
cqlsh -u 'my_username' -p 'my_password' -f /cassandra/kriptosare.cql
```

### Execute the analysis
See the paper "Cascading Machine Learning to Attack Bitcoin Anonimity" in order to generate the analysis that allow to build a model for entities caracterization. The results of this analysis are stored into the Cassandra DB/tables.
The script used into the research are stored into the ```analysis``` folder (file 1_, 2_, 3_). These script could be executed with the help of Jupyter Notebook (they are not automatized yet!)

### Run Web Server
Run the web server to querying the Database, so go into ```_viz``` folder and execute in a terminal
```
python web_app.py
```
After executing you have to open your browser and type the ip of your server (or localhost if you run the script locally) and the port :8810
[ip]:8810
Now the interface is ready.