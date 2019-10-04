## Kryptosare.class
The tool consists of four submodules, one of them private and three public: Behaviour trainer is private, while wallet Downloader, Behaviour predictor and REST-API are public. The wallet downloader allows us to download the whole blockchain, store data into a Database and compute a first elaboration of the Bitcoin data. The Behaviour trainer transforms the blockchain data extracting the features that the system needs during the analysis and when these data are ready, they are used for training the models creating the behaviour predictor. Then, the Behaviour predictor represents the trained model able to generate entity classification. The REST-API makes the prediction/classification available to the final users. The classification data is available through our own interface .

The tool is composed by Wallet downloader, Behaviour trainer, Behaviour predictor and the Rest-API. (Steps are verified in Ubuntu 16.04)

### 1 - Wallet downloader
Install Bitcoin Core:
	> apt-add-repository ppa:bitcoin/bitcoin
	> apt-get update
	> apt-get install bitcoin-qt

Execute the bitcoin daemon with the option rest
> bitcoind conf=.bitcoin/bitcoin.conf -rest=1

Then download the whole project from git
> git clone https://github.com/tv-vicomtech/Kriptosare.class.git

Install Docker version 17.12.1-ce
> sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
> curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add –
	>sudo apt-key fingerprint 0EBFCD88
> sudo add-apt-repository \ "deb [arch=amd64] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) \stable"
	> sudo apt-get update
	> sudo apt-get install docker-ce=17.12.1~ce-0~ubuntu
	> docker ps

Go into the folder project and execute the collector (you need python3)
	> cd Kriptosare.class/collector_mainnet
	> python3 generate_collectordata.py

The collector stores the whole blockchain in Cassandra tables stored inside the docker container

### 2 – Behaviour trainer (Private)
This is a private tool, so downloading the project in the folder Kriptosare.class/train_model/ the user can find the models already trained and ready to be used for testing (no source code available)
### 3 – Behaviour Predictor
Install Cassandra 
> echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
> curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
	> sudo apt-get update
	> sudo apt-get install Cassandra

Starting daemon
	> sudo service cassandra start

Load tables into keyspace
> cd Kriptosare.class/kryptosare_viz/cassandra
> cqlsh -f kriptosare.cql

Check the Java version (needed Java 8)
	> java -version

Install the Spark 2.3.4
	> wget https://archive.apache.org/dist/spark/spark-2.3.4/spark-2.3.4-bin-hadoop2.7.tgz
> tar xvzf spark-2.3.4-bin-hadoop2.7.tgz
> mv spark-2.3.4-bin-hadoop2.7/ opt/spark

Install the jupyter-notebook and some dependencies
	> pip3 install jupyter, pyspark, scikit-learn, numpy, pickle

Execute heuristcs code
	> cd Kriptosare.class/analysis/heuristic
> nohup jupyter nbconvert –execute transaction_data_converter.ipynb 
--ExecutePreprocessor.timeout=-1 &

> nohup jupyter nbconvert --execute heuristics.ipynb 
--ExecutePreprocessor.timeout=-1 &

Currently you have to wait the end of one task before executing the next one
Extract the Bitcoin transaction from the Cassandra and store it in csv:
	> cd Kriptosare.class/analysis/classification
> nohup jupyter nbconvert --execute data_processing_extract_bitcon.ipynb --ExecutePreprocessor.timeout=-1 

When the bitcoin cluster is ready, execute one by one the following code to obtain the final classification
> nohup jupyter nbconvert --execute data_processing_automatic.ipynb  --ExecutePreprocessor.timeout=-1

> nohup jupyter nbconvert –execute data_processing_multiclass.ipynb 
--ExecutePreprocessor.timeout=-1

4 – REST-API
Install the driver for connection python to Cassandra tables
	> pip3 install cassandra-driver

Got to the folder project and execute the REST-API in background
> cd Kriptosare.class/kryptosare_rest_api
> nohup python3 server_rest_api.py &

NB: In file server_rest_api.py, at the beginning, you have to set the variable cluster with the IP of the machine where Cassandra tables are stored! (default port = 9042)


### 5 – (optional) - Internal Interface
Install the python dependency
> pip3 install flask, requests, plotly or (apt-get install python-plotly)
Go to the folder project and execute the Interface in background
> cd Kriptosare.class/kryptosare_rest_api_viz
> nohup python3 server_krypto &

then, open your browser and digit the XXX.XXX.XXX.XXX:8810 where XXX.XXX.XXX.XXX is the IP of the machine where you have installed the Interface

NB: In file server_krypto.py, at the beginning, you have to set the variable url with the IP of the machine where the rest API is running! (default port = 5000)
