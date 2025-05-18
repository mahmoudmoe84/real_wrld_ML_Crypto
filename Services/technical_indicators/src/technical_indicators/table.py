

def create_table_in_risingwave(
    table_name: str,
    kafka_broker_address: str,
    kafka_topic: str,

):
    """
    create the table in the database with the given name inside risingwave and connect it to the kafka topic    
    this way risingwave automatically ingests messages from kafka  and updates the table in real time    
    """
    pass
