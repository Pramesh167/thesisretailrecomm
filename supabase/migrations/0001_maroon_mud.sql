/*
  # Initial Schema for Retail Store Optimization

  1. New Tables
    - `orders`: Stores order information
      - `order_id` (text, primary key): Unique order identifier
      - `customer_id` (text): Reference to customer
      - `created_at` (timestamp): Order creation timestamp
    
    - `products`: Stores product information
      - `product_id` (text, primary key): Unique product identifier
      - `category` (text): Product category
      - `sub_category` (text): Product sub-category
      - `current_position` (jsonb): Current position in store layout
      - `recommended_position` (jsonb): AI recommended position
    
    - `order_items`: Stores order line items
      - `id` (uuid, primary key): Unique identifier
      - `order_id` (text): Reference to order
      - `product_id` (text): Reference to product
      - `quantity` (integer): Quantity ordered
      - `sales` (numeric): Sales amount
      - `profit` (numeric): Profit amount

  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated users
*/

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
  order_id text PRIMARY KEY,
  customer_id text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
  product_id text PRIMARY KEY,
  category text NOT NULL,
  sub_category text NOT NULL,
  current_position jsonb DEFAULT '{"x": 0, "y": 0, "z": 0}'::jsonb,
  recommended_position jsonb DEFAULT '{"x": 0, "y": 0, "z": 0}'::jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id text REFERENCES orders(order_id),
  product_id text REFERENCES products(product_id),
  quantity integer NOT NULL CHECK (quantity > 0),
  sales numeric NOT NULL CHECK (sales >= 0),
  profit numeric NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Enable Row Level Security
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Allow authenticated users to read orders"
  ON orders FOR SELECT TO authenticated USING (true);

CREATE POLICY "Allow authenticated users to read products"
  ON products FOR SELECT TO authenticated USING (true);

CREATE POLICY "Allow authenticated users to update product positions"
  ON products FOR UPDATE TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow authenticated users to read order items"
  ON order_items FOR SELECT TO authenticated USING (true);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_sub_category ON products(sub_category);