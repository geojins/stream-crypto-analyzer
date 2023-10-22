
## Setup
* python -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt


## Submit Spark Job
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 main.py 