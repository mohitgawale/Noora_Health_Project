from utils.client import PostgresClient

def main():
    pclient = PostgresClient('prod')

    check_1_query = """
    SELECT s.*
    FROM whatsapp_data.msg_status s
    LEFT JOIN whatsapp_data.msg_info i ON s.message_id = i.id
    WHERE i.id IS NULL;
    """
    check_1_df = pclient.fetch(check_1_query)

    check_2_query = """
    SELECT i.*
    FROM whatsapp_data.msg_info i
    LEFT JOIN whatsapp_data.msg_status s ON i.id = s.message_id
    WHERE s.message_id IS NULL;
    """
    check_2_df = pclient.fetch(check_2_query)

    check_3_query = """
    SELECT s1.message_id, s1.status AS earlier_status, s1.inserted_at AS earlier_time,
           s2.status AS later_status, s2.inserted_at AS later_time
    FROM whatsapp_data.msg_status s1
    JOIN whatsapp_data.msg_status s2 ON s1.message_id = s2.message_id
    WHERE s1.status = 'read' AND s2.status = 'delivered' AND s1.inserted_at < s2.inserted_at;
    """
    check_3_df = pclient.fetch(check_3_query)

    check_4_query = """
    SELECT * FROM whatsapp_data.msg_info WHERE inserted_at > updated_at;
    """
    check_4_df = pclient.fetch(check_4_query)

if __name__ == "__main__":
    main()
