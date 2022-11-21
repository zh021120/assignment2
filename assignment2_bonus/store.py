import os
from supabase import create_client, Client

url: str = os.environ.get("https://qmamdjopqczccdglqoua.supabase.co")
key: str = os.environ.get("Zhanna2002nov")

supabase: Client = create_client(url, key)

def find_all_mames():
    data = supabase.table("users").select("*").execute()
    # Equivalent for SQL Query "SELECT * FROM games;"
    return data['data']

users = find_all_names()
