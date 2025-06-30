from utils.client import PostgresClient

def main():
    pclient = PostgresClient('prod')

    status_query = """
    CREATE TABLE IF NOT EXISTS whatsapp_data.msg_status (
        id BIGINT,
        status VARCHAR(20) NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        uuid UUID NOT NULL,
        message_uuid UUID NOT NULL,
        message_id BIGINT NOT NULL,
        number_id BIGINT NOT NULL,
        inserted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """

    message_query = """
    CREATE TABLE IF NOT EXISTS whatsapp_data.msg_info (
        id BIGINT,
        message_type VARCHAR(50),
        masked_addressees TEXT,
        masked_author VARCHAR(255),
        content TEXT,
        author_type VARCHAR(50),
        direction VARCHAR(20),
        external_id VARCHAR(255),
        external_timestamp TIMESTAMP,
        masked_from_addr VARCHAR(255),
        is_deleted BOOLEAN DEFAULT FALSE,
        last_status VARCHAR(50),
        last_status_timestamp TIMESTAMP,
        rendered_content TEXT,
        source_type VARCHAR(50),
        uuid UUID,
        inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    pclient.execute(message_query)
    pclient.execute(status_query)

if __name__ == "__main__":
    main()
