import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils.client import PostgresClient, GoogleSheetClient

def make_autopct(values):
    def _autopct(pct):
        total = sum(values)
        count = int(round(pct * total / 100.0))
        return f'{pct:.1f}%\n({count})'
    return _autopct

def main():
    sns.set(style='whitegrid')
    pclient = PostgresClient('prod')
    gclient = GoogleSheetClient('gdrive_filename')

    # Q1
    q1_query = """
    WITH A AS (
        SELECT s.number_id, i.direction
        FROM whatsapp_data.msg_info i
        LEFT JOIN whatsapp_data.msg_status s ON i.id = s.message_id
        WHERE DATE(i.inserted_at) >= DATE('2024-04-02') - 180
    )
    SELECT COUNT(DISTINCT number_id) AS total_users FROM A;
    """
    q1_query_df = pclient.fetch(q1_query)

    # Q2
    send_vs_read_query = """
    SELECT s.message_id, s.status
    FROM whatsapp_data.msg_info i
    LEFT JOIN whatsapp_data.msg_status s ON i.id = s.message_id
    WHERE i.direction = 'outbound';
    """
    send_vs_read_df = pclient.fetch(send_vs_read_query)

    filtered_df = send_vs_read_df[send_vs_read_df['status'].isin(['sent', 'read'])]
    status_per_message = filtered_df.groupby('message_id')['status'].apply(set).reset_index()
    status_per_message['is_read'] = status_per_message['status'].apply(lambda x: 'read' in x)

    read_count = status_per_message['is_read'].sum()
    total_non_failed = len(status_per_message)

    plt.figure(figsize=(6, 6))
    plt.pie(
        [read_count, total_non_failed - read_count],
        labels=['Read', 'Not Read'],
        autopct='%1.1f%%',
        startangle=90,
        colors=['#66b3ff', '#ff9999']
    )
    plt.title('Fraction of Non-Failed Outbound Messages That Were Read')
    plt.tight_layout()
    plt.show()

    # Q3
    status_df = gclient.read_sheet(
        spreadsheet_id='1DsqujADFh2MNkfpTsWi5bzZIySlKMORRk41p908QHAE',
        worksheet_name='Statuses'
    )
    read_time_diff_df = status_df[status_df['status'].isin(['sent', 'read'])]
    pivot_df = read_time_diff_df.pivot_table(
        index='message_id', columns='status', values='inserted_at', aggfunc='first'
    )
    pivot_df['time_to_read'] = (
        pd.to_datetime(pivot_df['read']) - pd.to_datetime(pivot_df['sent'])
    ).dt.total_seconds()
    pivot_df.dropna(subset=['sent', 'read'], inplace=True)

    pivot_df['time_to_read'].plot(kind='hist', bins=30, color='orange', title='Time to Read Message')
    plt.xlabel("Seconds to Read")
    plt.ylabel("Message Count")
    plt.tight_layout()
    plt.show()

    # Q4
    q4_query = """
    SELECT 
        CASE WHEN i.last_status IS NULL THEN 'No_Status' ELSE i.last_status END AS status,
        COUNT(DISTINCT id) AS cnt
    FROM whatsapp_data.msg_info i
    WHERE i.direction = 'outbound'
    AND DATE(inserted_at) >= DATE('2024-04-22') - 7
    GROUP BY 1;
    """
    q4_query_df = pclient.fetch(q4_query)

    plt.figure(figsize=(7, 7))
    plt.pie(
        q4_query_df['cnt'],
        labels=q4_query_df['status'],
        autopct=make_autopct(q4_query_df['cnt']),
        startangle=90,
        colors=plt.cm.Pastel1.colors
    )
    plt.title('Message Status Distribution')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
