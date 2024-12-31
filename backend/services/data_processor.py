import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from typing import Dict, List
import os
from datetime import datetime

class DataProcessor:
    def __init__(self, file_path: str, db):
        self.file_path = file_path
        self.db = db
        self.required_columns = [
            'Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
            'Customer ID', 'Customer Name', 'Segment', 'Country/Region',
            'City', 'State/Province', 'Postal Code', 'Region',
            'Product ID', 'Sub-Category', 'Product Name',
            'Sales', 'Quantity', 'Discount', 'Profit'
        ]
        # Log the file upload attempt
        self.db.add_file_history(os.path.basename(file_path))
        try:
            self.df = self._read_file()
            self.db.update_file_status(os.path.basename(file_path), 'Reading_Success')
        except Exception as e:
            self.db.update_file_status(os.path.basename(file_path), 'Reading_Failed', str(e))
            raise

    def _read_file(self) -> pd.DataFrame:
        file_ext = os.path.splitext(self.file_path)[1].lower()

        try:
            if file_ext == '.xlsx':
                return pd.read_excel(self.file_path)
            elif file_ext == '.xls':
                return pd.read_excel(self.file_path, engine='xlrd')
            elif file_ext == '.csv':
                return pd.read_csv(self.file_path)
            elif file_ext == '.txt':
                delimiters = [',', '\t', '|', ';']
                for delimiter in delimiters:
                    try:
                        df = pd.read_csv(self.file_path, delimiter=delimiter)
                        if len(df.columns) > 1:
                            return df
                    except:
                        continue
                raise ValueError("Could not parse TXT file with common delimiters")
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")

    def clean_data(self) -> pd.DataFrame:
        try:
            missing_cols = [col for col in self.required_columns if col not in self.df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

            cleaned_df = self.df[self.required_columns].copy()
            cleaned_df = cleaned_df.drop_duplicates()
            # cleaned_df = cleaned_df.dropna()

            # Convert date columns to datetime
            date_columns = ['Order Date', 'Ship Date']
            for col in date_columns:
                cleaned_df[col] = pd.to_datetime(cleaned_df[col])

            # Convert numeric columns
            numeric_columns = ['Sales', 'Quantity', 'Discount', 'Profit']
            for col in numeric_columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')

            cleaned_df = cleaned_df.dropna()

            self.db.update_file_status(os.path.basename(self.file_path), 'Cleaning_Success')
            return cleaned_df
        except Exception as e:
            self.db.update_file_status(os.path.basename(self.file_path), 'Cleaning_Failed', str(e))
            raise

    def save_cleaned_data(self):
        """
        Save normalized data after storing customers, products, and sales.
        """
        try:
            # Clear previous data before inserting new data
            self.db.clear_previous_data()

            cleaned_df = self.clean_data()

            # Save customers data
            customers_data = self.get_customers_data()
            for customer in customers_data:
                self.db.add_customer(customer)

            # Save products data
            products_data = self.get_products_data()
            for product in products_data:
                self.db.add_product(product)

            # Save sales data
            sales_data = self.get_sales_data()
            for sale in sales_data:
                self.db.add_sale(sale)

            # Save normalized data
            for _, row in cleaned_df.iterrows():
                self.db.store_normalized_data({
                    'order_id': row['Order ID'],
                    'customer_id': row['Customer ID'],
                    'product_id': row['Product ID'],
                    'sub_category': row['Sub-Category'],
                    'sales': float(row['Sales']),
                    'quantity': int(row['Quantity']),
                    'profit': float(row['Profit'])
                })

            self.db.update_file_status(os.path.basename(self.file_path), 'Processing_Success')
        except Exception as e:
            self.db.update_file_status(os.path.basename(self.file_path), 'Processing_Failed', str(e))
            raise

    def get_customers_data(self) -> List[Dict]:
        cleaned_df = self.clean_data()
        customers_data = []
        for _, row in cleaned_df.drop_duplicates(subset=['Customer ID']).iterrows():
            customer_data = {
                'customer_id': row['Customer ID'],
                'customer_name': row['Customer Name'],
                'segment': row['Segment'],
                'country': row['Country/Region'],
                'region': row['Region'],
                'city': row['City'],
                'state_province': row['State/Province'],
                'postal_code': str(row['Postal Code'])  # Convert to string for consistency
            }
            customers_data.append(customer_data)
        return customers_data

    def get_products_data(self) -> List[Dict]:
        cleaned_df = self.clean_data()
        products_data = []
        for _, row in cleaned_df.drop_duplicates(subset=['Product ID']).iterrows():
            product_data = {
                'product_id': row['Product ID'],
                'sub_category': row['Sub-Category'],  # Changed from 'Category' to 'Sub-Category'
                'product_name': row['Product Name']
            }
            products_data.append(product_data)
        return products_data

    def get_sales_data(self) -> List[Dict]:
        cleaned_df = self.clean_data()
        sales_data = []
        for _, row in cleaned_df.iterrows():
            sale_data = {
                'order_id': row['Order ID'],
                'customer_id': row['Customer ID'],
                'product_id': row['Product ID'],
                'sales': float(row['Sales']),
                'quantity': int(row['Quantity']),
                'discount': float(row['Discount']),
                'profit': float(row['Profit'])
            }
            sales_data.append(sale_data)
        return sales_data

    def analyze_data(self) -> Dict:
        try:
            cleaned_df = self.clean_data()

            metrics = {
                'total_sales': float(cleaned_df['Sales'].sum()),
                'total_profit': float(cleaned_df['Profit'].sum()),
                'average_order_value': float(cleaned_df.groupby('Order ID')['Sales'].sum().mean()),
                'total_orders': cleaned_df['Order ID'].nunique(),
                'total_products': cleaned_df['Product ID'].nunique(),
                'average_discount': float(cleaned_df['Discount'].mean()),
                'profit_margin': float((cleaned_df['Profit'].sum() / cleaned_df['Sales'].sum()) * 100)
            }

            # Fix for sub-category analysis - no multi-index
            sub_category_analysis = {}
            sub_category_metrics = cleaned_df.groupby('Sub-Category').agg({
                'Sales': 'sum',
                'Profit': 'sum',
                'Quantity': 'sum',
                'Discount': 'mean'
            }).round(2)

            for sub_category in sub_category_metrics.index:
                sub_category_analysis[sub_category] = {
                    'Sales': float(sub_category_metrics.loc[sub_category, 'Sales']),
                    'Profit': float(sub_category_metrics.loc[sub_category, 'Profit']),
                    'Quantity': float(sub_category_metrics.loc[sub_category, 'Quantity']),
                    'Discount': float(sub_category_metrics.loc[sub_category, 'Discount'])
                }

            # Fix for product performance - handle multi-index properly
            product_metrics = cleaned_df.groupby(['Product ID', 'Product Name']).agg({
                'Sales': 'sum',
                'Profit': 'sum',
                'Quantity': 'sum',
                'Discount': 'mean'
            }).round(2).sort_values('Sales', ascending=False).head(10)

            top_products = {}
            for (product_id, product_name) in product_metrics.index:
                key = f"{product_id}_{product_name}"  # Create a string key
                top_products[key] = {
                    'product_id': product_id,
                    'product_name': product_name,
                    'Sales': float(product_metrics.loc[(product_id, product_name), 'Sales']),
                    'Profit': float(product_metrics.loc[(product_id, product_name), 'Profit']),
                    'Quantity': float(product_metrics.loc[(product_id, product_name), 'Quantity']),
                    'Discount': float(product_metrics.loc[(product_id, product_name), 'Discount'])
                }

            results = {
                'metrics': metrics,
                'sub_category_analysis': sub_category_analysis,  # Changed from category_analysis to sub_category_analysis
                'top_products': top_products
            }

            # Store analysis results in database
            self.db.store_analysis_results(results)
            return results
        except Exception as e:
            self.db.update_file_status(os.path.basename(self.file_path), 'Analysis_Failed', str(e))
            raise

    def generate_layout_recommendations(self) -> Dict:
        try:
            cleaned_df = self.clean_data()

            # Calculate metrics using Sub-Category instead of Category
            product_metrics = cleaned_df.groupby('Product ID').agg({
                'Product Name': 'first',  # Take the first product name
                'Sub-Category': 'first',  # Use Sub-Category instead of Category
                'Sales': 'sum',
                'Profit': 'sum',
                'Quantity': 'sum',
                'Discount': 'mean',
            }).reset_index()

            scaler = StandardScaler()
            features = scaler.fit_transform(product_metrics[['Sales', 'Profit', 'Quantity', 'Discount']])

            kmeans = KMeans(n_clusters=4, random_state=42)
            product_metrics['cluster'] = kmeans.fit_predict(features)

            recommendations = {}
            for _, row in product_metrics.iterrows():
                section = (row['cluster'] * 4) + (len(recommendations) % 4)
                recommendations[row['Product ID']] = {
                    'product_name': row['Product Name'],
                    'sub_category': row['Sub-Category'],  # Ensure Sub-Category is included
                    'section': int(section),  # Ensure section is an integer
                    'priority': 'high' if row['Profit'] > product_metrics['Profit'].median() else 'medium'
                }

            # Store recommendations in the database
            self.db.store_layout_recommendations(recommendations)
            return recommendations
        except Exception as e:
            self.db.update_file_status(os.path.basename(self.file_path), 'Layout_Recommendation_Failed', str(e))
            raise

    def market_basket_analysis(self) -> List[Dict]:
        try:
            transactions = self.df.groupby(['Order ID'])['Product Name'].apply(list).tolist()

            te = TransactionEncoder()
            te_ary = te.fit(transactions).transform(transactions)
            df = pd.DataFrame(te_ary, columns=te.columns_)

            frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)
            rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

            results = []
            for _, rule in rules.iterrows():
                results.append({
                    'antecedents': list(rule['antecedents']),
                    'consequents': list(rule['consequents']),
                    'support': float(rule['support']),
                    'confidence': float(rule['confidence']),
                    'lift': float(rule['lift'])
                })

            return results
        except Exception as e:
            self.db.update_file_status(os.path.basename(self.file_path), 'Market_Basket_Analysis_Failed', str(e))
            raise
