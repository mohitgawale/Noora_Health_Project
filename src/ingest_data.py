from utils.client import GoogleSheetClient, PostgresClient

def main():
    gclient = GoogleSheetClient('gdrive_filename')
    pclient = PostgresClient('prod')

    messages_df = gclient.read_sheet(
        spreadsheet_id='1DsqujADFh2MNkfpTsWi5bzZIySlKMORRk41p908QHAE',
        worksheet_name='Messages'
    )
    status_df = gclient.read_sheet(
        spreadsheet_id='1DsqujADFh2MNkfpTsWi5bzZIySlKMORRk41p908QHAE',
        worksheet_name='Statuses'
    )

    pclient.load_dataframe(messages_df, 'whatsapp_data.msg_info', refresh=False)
    pclient.load_dataframe(status_df, 'whatsapp_data.msg_status', refresh=False)

if __name__ == "__main__":
    main()

