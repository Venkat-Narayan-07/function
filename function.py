import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.storage.queue import QueueService

def main(myblob: func.InputStream):
    # Replace with your Queue SAS URL
    queue_sas_url = "https://27mar24storageaccount.queue.core.windows.net/?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-03-27T20:24:24Z&st=2024-03-27T12:24:24Z&spr=https&sig=Y7%2BkjvBrRcZATExOF27AC4kgd0z9TAITWhDIB2iYsqU%3D"
    
    # Replace with your Table SAS URL
    table_sas_url = "https://27mar24storageaccount.table.core.windows.net/?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-03-27T20:24:24Z&st=2024-03-27T12:24:24Z&spr=https&sig=Y7%2BkjvBrRcZATExOF27AC4kgd0z9TAITWhDIB2iYsqU%3D"

    # Connect to table storage
    table_service = TableService(endpoint_suffix="", sas_token=table_sas_url)
    
    # Connect to queue storage
    queue_service = QueueService(endpoint_suffix="", sas_token=queue_sas_url)

    # Retrieve the latest entry from the table storage
    latest_entry = table_service.query_entities("tickettable", filter="PartitionKey eq 'partition key'", top=1, orderby="Timestamp desc")

    # Extract ticket number from the latest entry
    if latest_entry:
        ticket_number = latest_entry[0].TicketNumber
        # Push the ticket number to the queue
        queue_service.put_message("ticketqueue", ticket_number)
        print(f"Ticket number {ticket_number} pushed to the queue.")
    else:
        print("No new entry found in the table.")
