import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple
import os

class DataProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.required_columns = [
            'Order ID', 
            'Customer ID', 
            'Product ID', 
            'Category', 
            'Sub-Category', 
            'Sales', 
            'Quantity', 
            'Profit'
        ]
        self.df = self._read_file()
        
    def _read_file(self) -> pd.DataFrame:
        """Read data file based on its extension."""
        file_ext = os.path.splitext(self.file_path)[1].lower()
        
        try:
            if file_ext == '.xlsx':
                return pd.read_excel(self.file_path)
            elif file_ext == '.xls':
                return pd.read_excel(self.file_path, engine='xlrd')
            elif file_ext == '.csv':
                return pd.read_csv(self.file_path)
            elif file_ext == '.txt':
                # Try common delimiters
                delimiters = [',', '\t', '|', ';']
                for delimiter in delimiters:
                    try:
                        df = pd.read_csv(self.file_path, delimiter=delimiter)
                        if len(df.columns) > 1:  # Successfully parsed with multiple columns
                            return df
                    except:
                        continue
                raise ValueError("Could not parse TXT file with common delimiters")
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")
        
    def clean_data(self) -> pd.DataFrame:
        """Clean and prepare the data for processing."""
        try:
            # Ensure required columns exist
            missing_cols = [col for col in self.required_columns if col not in self.df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
            
            # Select only required columns
            cleaned_df = self.df[self.required_columns].copy()
            
            # Remove duplicates
            cleaned_df = cleaned_df.drop_duplicates()
            
            # Handle missing values
            cleaned_df = cleaned_df.dropna()
            
            # Convert numeric columns
            numeric_columns = ['Sales', 'Quantity', 'Profit']
            for col in numeric_columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
                
            # Drop rows with invalid numeric values
            cleaned_df = cleaned_df.dropna()
            
            return cleaned_df
        except Exception as e:
            raise ValueError(f"Error cleaning data: {str(e)}")
    
    def analyze_data(self) -> Dict:
        """Generate insights from the cleaned data."""
        cleaned_df = self.clean_data()
        
        # Calculate key metrics
        metrics = {
            'total_sales': float(cleaned_df['Sales'].sum()),
            'total_profit': float(cleaned_df['Profit'].sum()),
            'average_order_value': float(cleaned_df.groupby('Order ID')['Sales'].sum().mean()),
            'total_orders': int(cleaned_df['Order ID'].nunique()),
            'total_products': int(cleaned_df['Product ID'].nunique())
        }
        
        # Category analysis
        category_analysis = cleaned_df.groupby('Category').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).round(2).to_dict('index')
        
        # Product performance
        product_performance = cleaned_df.groupby('Product ID').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).round(2).sort_values('Sales', ascending=False).head(10).to_dict('index')
        
        return {
            'metrics': metrics,
            'category_analysis': category_analysis,
            'top_products': product_performance
        }
    
    def generate_layout_recommendations(self) -> Dict:
        """Generate store layout recommendations based on product performance."""
        cleaned_df = self.clean_data()
        
        # Calculate product metrics for clustering
        product_metrics = cleaned_df.groupby('Product ID').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        
        # Normalize metrics for clustering
        scaler = StandardScaler()
        features = scaler.fit_transform(product_metrics[['Sales', 'Profit', 'Quantity']])
        
        # Perform clustering
        kmeans = KMeans(n_clusters=4, random_state=42)
        product_metrics['cluster'] = kmeans.fit_predict(features)
        
        # Generate position recommendations
        recommendations = {}
        for cluster in range(4):
            cluster_products = product_metrics[product_metrics['cluster'] == cluster]
            section_start = cluster * 4
            
            for idx, (_, product) in enumerate(cluster_products.iterrows()):
                section = section_start + (idx % 4)
                recommendations[product['Product ID']] = {
                    'section': section,
                    'priority': 'high' if product['Profit'] > product_metrics['Profit'].median() else 'medium'
                }
        
        return recommendations