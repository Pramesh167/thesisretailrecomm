import psycopg2
from psycopg2.extras import Json
from typing import Dict, List

class Database:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int = 5000):
        try:
            self.conn = psycopg2.connect(
                dbname="retail_store",
                user="postgres",
                password="postgres",
                host="localhost",
                port=5000
            )
            self.create_tables()
        except Exception as e:
            raise ValueError(f"Database initialization failed: {e}")

    def create_tables(self):
        with self.conn.cursor() as cur:
            # Customers Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id SERIAL PRIMARY KEY,
                    customer_name TEXT NOT NULL,
                    segment TEXT NOT NULL,
                    country TEXT NOT NULL,
                    region TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state_province TEXT NOT NULL,
                    postal_code TEXT NOT NULL
                )
            """)

            # Products Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    sub_category TEXT NOT NULL,
                    product_name TEXT NOT NULL
                )
            """)

            # Sales Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    sales_id SERIAL PRIMARY KEY,
                    customer_id INTEGER REFERENCES customers(customer_id),
                    product_id TEXT REFERENCES products(product_id),
                    sales NUMERIC NOT NULL,
                    quantity INTEGER NOT NULL,
                    discount NUMERIC NOT NULL,
                    profit NUMERIC NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Normalized Data Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS normalized_data (
                    id SERIAL PRIMARY KEY,
                    order_id TEXT NOT NULL,
                    customer_id INTEGER REFERENCES customers(customer_id),
                    product_id TEXT REFERENCES products(product_id),
                    category TEXT NOT NULL,
                    sub_category TEXT NOT NULL,
                    sales NUMERIC NOT NULL,
                    quantity INTEGER NOT NULL,
                    profit NUMERIC NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Layout Recommendations Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS layout_recommendations (
                    id SERIAL PRIMARY KEY,
                    product_id TEXT REFERENCES products(product_id),
                    section INTEGER NOT NULL,
                    priority TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Analytics Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id SERIAL PRIMARY KEY,
                    metrics JSONB NOT NULL,
                    category_analysis JSONB NOT NULL,
                    top_products JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # File Upload History Table
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS file_history (
                                id SERIAL PRIMARY KEY,
                                filename TEXT NOT NULL,
                                status TEXT NOT NULL,
                                error_message TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        """)

            self.conn.commit()

    def add_customer(self, customer_data: Dict):
        """Add a customer record."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO customers (customer_name, segment, country, region, city, state_province, postal_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                customer_data['customer_name'],
                customer_data['segment'],
                customer_data['country'],
                customer_data['region'],
                customer_data['city'],
                customer_data['state_province'],
                customer_data['postal_code']
            ))
            self.conn.commit()

    def add_product(self, product_data: Dict):
        """Add a product record."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO products (product_id, category, sub_category, product_name)
                VALUES (%s, %s, %s, %s)
            """, (
                product_data['product_id'],
                product_data['category'],
                product_data['sub_category'],
                product_data['product_name']
            ))
            self.conn.commit()

    def add_sale(self, sale_data: Dict):
        """Add a sale record."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sales (customer_id, product_id, sales, quantity, discount, profit)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                sale_data['customer_id'],
                sale_data['product_id'],
                sale_data['sales'],
                sale_data['quantity'],
                sale_data['discount'],
                sale_data['profit']
            ))
            self.conn.commit()

    def store_normalized_data(self, normalized_data: Dict):
        """Store normalized data."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO normalized_data (order_id, customer_id, product_id, category, sub_category, sales, quantity, profit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                normalized_data['order_id'],
                normalized_data['customer_id'],
                normalized_data['product_id'],
                normalized_data['category'],
                normalized_data['sub_category'],
                normalized_data['sales'],
                normalized_data['quantity'],
                normalized_data['profit']
            ))
            self.conn.commit()

    def store_layout_recommendations(self, recommendations: Dict):
        """Store layout recommendations."""
        with self.conn.cursor() as cur:
            for product_id, data in recommendations.items():
                cur.execute("""
                    INSERT INTO layout_recommendations (product_id, section, priority)
                    VALUES (%s, %s, %s)
                """, (product_id, data['section'], data['priority']))
            self.conn.commit()

    def store_analysis_results(self, results: Dict):
        """Store analysis results."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO analysis_results (metrics, category_analysis, top_products)
                VALUES (%s, %s, %s)
            """, (
                Json(results['metrics']),
                Json(results['category_analysis']),
                Json(results.get('top_products', {}))
            ))
            self.conn.commit()

    def fetch_normalized_data(self) -> List[Dict]:
        """Fetch all normalized data."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM normalized_data
            """)
            rows = cur.fetchall()
            return [{
                'id': row[0],
                'order_id': row[1],
                'customer_id': row[2],
                'product_id': row[3],
                'category': row[4],
                'sub_category': row[5],
                'sales': row[6],
                'quantity': row[7],
                'profit': row[8],
                'created_at': row[9]
            } for row in rows]

    def fetch_layout_recommendations(self) -> List[Dict]:
        """Fetch all layout recommendations."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT product_id, section, priority
                FROM layout_recommendations
            """)
            rows = cur.fetchall()
            return [{
                'product_id': row[0],
                'section': row[1],
                'priority': row[2]
            } for row in rows]

    def fetch_analysis_results(self) -> List[Dict]:
        """Fetch all analysis results."""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT metrics, category_analysis, top_products
                FROM analysis_results
                ORDER BY created_at DESC LIMIT 1
            """)
            row = cur.fetchone()
            return {
                'metrics': row[0],
                'category_analysis': row[1],
                'top_products': row[2]
            } if row else {}


    def add_file_history(self, filename: str):
        """Log the file upload in the file history table."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO file_history (filename, status)
                VALUES (%s, %s)
            """, (filename, 'Pending'))  # Set initial status as 'Pending'
            self.conn.commit()

    def update_file_status(self, filename: str, status: str, error_message: str = None):
        """Update the status of the uploaded file."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    UPDATE file_history
                    SET status = %s, error_message = %s
                    WHERE filename = %s
                """, (status, error_message, filename))
                self.conn.commit()
        except Exception as e:
            print(f"Error updating file status for {filename}: {e}")
            self.conn.rollback()  # Rollback in case of an error

    def clear_previous_data(self):
        """
        Clears all data from the relevant tables except the file history table.
        """
        try:
            # List of tables to clear (excluding 'file_history')
            tables_to_clear = ['customers', 'products', 'sales', 'analysis_results', 'layout_recommendations']

            for table in tables_to_clear:
                with self.conn.cursor() as cur:
                    # Corrected the query to properly include the table name
                    cur.execute(f"DELETE FROM {table};")
                    self.conn.commit()

            print("Data cleared successfully from the relevant tables.")

        except Exception as e:
            print(f"Error clearing previous data: {e}")
            self.conn.rollback()  # Rollback in case of an error
