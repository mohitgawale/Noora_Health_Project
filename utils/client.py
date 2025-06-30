import os
import json
import configparser
import pandas as pd
from tqdm import tqdm
import psycopg2
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetClient:
    def __init__(self, gdrive_filename):
        """
        Initializes the GoogleSheetClient with service account credentials from a config file.

        Args:
            gdrive_filename (str): Section name in credentials.ini containing the path to the JSON key.
        """
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
            'https://spreadsheets.google.com/feeds'
        ]
        self.gdrive_filename = gdrive_filename
        self.creds = self._load_creds()
        self.client = gspread.authorize(self.creds)

    def _load_creds(self):
        """
        Loads the JSON key credentials from the configuration file.

        Returns:
            ServiceAccountCredentials: Google service account credentials.
        """
        path = os.path.join(os.getcwd(), 'config', 'credentials.ini') 
        config = configparser.ConfigParser()
        config.read(path)
        json_key = config[self.gdrive_filename]['json_key']
        return ServiceAccountCredentials.from_json_keyfile_name(json_key, self.scopes)

    def read_sheet(self, spreadsheet_id, worksheet_name):
        """
        Reads data from a specific worksheet in a Google Spreadsheet.

        Args:
            spreadsheet_id (str): Google Sheets document ID.
            worksheet_name (str): Name of the worksheet.

        Returns:
            pd.DataFrame: Data from the sheet as a DataFrame.
        """
        sheet = self.client.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        data = sheet.get_all_values()
        df = pd.DataFrame(data)
        df.columns = df.iloc[0]
        return df[1:].reset_index(drop=True)

    def write_sheet(self, spreadsheet_id, worksheet_name, df):
        """
        Writes a DataFrame to a specific worksheet in a Google Spreadsheet.

        Args:
            spreadsheet_id (str): Google Sheets document ID.
            worksheet_name (str): Name of the worksheet.
            df (pd.DataFrame): Data to be written to the worksheet.
        """
        sheet = self.client.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        sheet.clear()
        sheet.update([df.columns.tolist()] + df.values.tolist())


class PostgresClient:
    def __init__(self, db_config_name):
        """
        Initializes the PostgresClient with database credentials from a config file.

        Args:
            db_config_name (str): Section name in credentials.ini containing DB connection parameters.
        """
        self.config = self._load_config(db_config_name)
        self.conn = psycopg2.connect(**self.config)

    def _load_config(self, db_name):
        """
        Loads database configuration from credentials.ini.

        Args:
            db_name (str): Section name in config file.

        Returns:
            dict: Database connection parameters.
        """
        path = os.path.join(os.getcwd(), 'config', 'credentials.ini')  
        config = configparser.ConfigParser()
        config.read(path)
        creds = config[db_name]
        return {
            'host': creds['hostname'],
            'dbname': creds['database'],
            'user': creds['username'],
            'port': creds['port'],
            'password': creds['password']
        }

    def execute(self, query):
        """
        Executes a SQL query (e.g., INSERT, TRUNCATE, UPDATE).

        Args:
            query (str): SQL query to execute.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(query)
                self.conn.commit()
        except Exception as e:
            print(f"ERROR executing query: {e}")

    def fetch(self, query):
        """
        Executes a SELECT query and returns the results as a DataFrame.

        Args:
            query (str): SQL SELECT query.

        Returns:
            pd.DataFrame: Query results.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        except Exception as e:
            print(f"ERROR fetching query: {e}")
            return pd.DataFrame()

    def load_dataframe(self, df, table, refresh=False, chunksize=10000):
        """
        Loads a DataFrame into a PostgreSQL table, optionally truncating before loading.

        Args:
            df (pd.DataFrame): Data to load.
            table (str): Target table name.
            refresh (bool): Whether to truncate table before loading. Default is False.
            chunksize (int): Number of rows per insert batch. Default is 10000.
        """
        if df.empty:
            print("No data to load.")
            return

        df = self._sanitize_df(df)

        if refresh:
            print(f"Truncating {table}...")
            self.execute(f"TRUNCATE TABLE {table}")

        for i in tqdm(range(0, len(df), chunksize)):
            chunk = df.iloc[i:i+chunksize]
            if not chunk.empty:
                rows = [tuple(x.values()) for x in chunk.to_dict('records')]
                values = ', '.join(
                    str(r).replace("''", "null")
                         .replace("'NaT'", "null")
                         .replace("'nan'", "null")
                         .replace("'None'", "null")
                         .replace("'<NA>'", "null")
                    for r in rows
                )
                columns = ', '.join(df.columns)
                query = f"INSERT INTO {table} ({columns}) VALUES {values}"
                self.execute(query)

        print(f"{table} loaded with {len(df)} rows.\n")

    def _sanitize_df(self, df):
        """
        Cleans column names and escapes quotes in data.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: Sanitized DataFrame.
        """
        df.columns = [c.replace(' ', '_').lower() for c in df.columns]
        return df.applymap(lambda x: str(x).replace("'", '"') if pd.notna(x) else x)