from google.cloud import storage, bigquery

# storage_client = storage.Client.from_service_account_json('vnstock-381809-22dc568a0a39.json')
# storage_client.create_bucket('vnstock-data')
# bucket = storage_client.get_bucket('vnstock-data')
# bucket.blob('data.csv').upload_from_filename('data.csv')
# print('Create GSC done!')

client = bigquery.Client.from_service_account_json('vnstock-381809-22dc568a0a39.json')
dataset_name = 'vnstock'
# table_name = 'vnstock_data'
table_name = 'test'

dataset_ref = client.dataset(dataset_name)
dataset = bigquery.Dataset(client.dataset(dataset_name))
# dataset = client.create_dataset(dataset)

# Define BigQuery schema
job_config = bigquery.LoadJobConfig()
job_config.schema = [
    bigquery.SchemaField('Open', 'FLOAT', mode='NULLABLE'),
    bigquery.SchemaField('High', 'FLOAT', mode='NULLABLE'),
    bigquery.SchemaField('Low', 'FLOAT', mode='NULLABLE'),
    bigquery.SchemaField('Close', 'FLOAT', mode='NULLABLE'),
    bigquery.SchemaField('Volume', 'FLOAT', mode='NULLABLE'),
    bigquery.SchemaField('TradingDate', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('Ticker', 'STRING', mode='NULLABLE'),
]

job_config.skip_leading_rows = 1
job_config.source_format = bigquery.SourceFormat.CSV

uri = 'gs://vnstock-data/data.csv'

load_job = client.load_table_from_uri(
                uri,
                dataset_ref.table(table_name),
                job_config=job_config)

load_job.result()  # wait for table load to complete.
print('Job finished.')

destination_table = client.get_table(dataset_ref.table(table_name))
print('Loaded {} rows.'.format(destination_table.num_rows))
