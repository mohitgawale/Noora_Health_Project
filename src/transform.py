from utils.client import PostgresClient

def main():
    pclient = PostgresClient('prod')

    total_rows_query = """
    SELECT *, ROW_NUMBER() OVER(PARTITION BY i.id, i.content ORDER BY s.id) AS row_num
    FROM whatsapp_data.msg_info i
    LEFT JOIN whatsapp_data.msg_status s ON i.id = s.message_id;
    """
    total_rows_df = pclient.fetch(total_rows_query)

    dup_record_query = """
    WITH A AS (
        SELECT *, ROW_NUMBER() OVER(PARTITION BY i.id, i.content ORDER BY s.id) AS row_num
        FROM whatsapp_data.msg_info i
        LEFT JOIN whatsapp_data.msg_status s ON i.id = s.message_id
    )
    SELECT * FROM A WHERE row_num > 1;
    """
    dup_record_df = pclient.fetch(dup_record_query)

if __name__ == "__main__":
    main()
