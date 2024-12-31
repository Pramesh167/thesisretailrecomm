from data_processor import DataProcessor
from supabase_uploader import SupabaseUploader

def main():
    try:
        # Initialize data processor
        processor = DataProcessor('Sample_Superstore.xlsx')
        
        # Process and prepare data
        prepared_data = processor.prepare_for_supabase()
        
        # Upload to Supabase
        uploader = SupabaseUploader()
        uploader.upload_data(prepared_data)
        
        print("Data successfully processed and uploaded to Supabase!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()