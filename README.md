# crypto-analysis

Does on-chain analysis of bitcoin and analyzes the likelihood of impermanent loss in yield farming cryptocurrencies.

**packages in src directory:**

* api - Contains classes for connecting to APIs.
* functions - Contains various functions, which take dataframes of prices, volumes, market caps, etc. as arguments and compute something.
* visualization - Functions, which help with the vizualization of data obtained by the APIs and functions from functions package.

**notebooks in src directory:**
* correlation_analysis.ipynb - Shows vizualization of how some cryptocurrencies' prices and returns correlate.
* impermanent_loss.ipynb - Computes the impermanent loss of yield farming assuming that the amount of assets in the pool remains constant.
* realized_metrics.ipynb - Vizualizes some on-chain metrics for bitcoin.
* trial-and-error.ipynb - Notebook for trying out new stuff.

**requirements:**

* Python version 3.9.7
* ipykernel
* numpy==1.20.3
* requests==2.26.0
* python-dateutil==2.8.2
* pandas==1.3.4
* matplotlib==3.4.3
* seaborn==0.11.2
