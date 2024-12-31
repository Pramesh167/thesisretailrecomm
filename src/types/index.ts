export interface Product {
  product_id: string;
  category: string;
  sub_category: string;
  current_position: Position;
  recommended_position: Position;
  created_at: string;
  updated_at: string;
}

export interface Position {
  x: number;
  y: number;
  z: number;
}

export interface Order {
  order_id: string;
  customer_id: string;
  created_at: string;
}

export interface OrderItem {
  id: string;
  order_id: string;
  product_id: string;
  quantity: number;
  sales: number;
  profit: number;
  created_at: string;
}