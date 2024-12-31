from typing import Dict, List
import os
from supabase import create_client, Client

class SupabaseUploader:
    def __init__(self):
        url = os.environ.get("VITE_SUPABASE_URL")
        key = os.environ.get("VITE_SUPABASE_ANON_KEY")
        if not url or not key:
            raise ValueError("Missing Supabase credentials")
        self.supabase: Client = create_client(url, key)
    
    def upload_data(self, data: Dict[str, List[Dict]]) -> None:
        """Upload data to respective Supabase tables."""
        # Upload products
        for product in data['products']:
            product['current_position'] = {'x': 0, 'y': 0, 'z': 0}
            product['recommended_position'] = {'x': 0, 'y': 0, 'z': 0}
            self.supabase.table('products').upsert(product).execute()
        
        # Upload orders
        self.supabase.table('orders').upsert(data['orders']).execute()
        
        # Upload order items
        self.supabase.table('order_items').upsert(data['order_items']).execute()