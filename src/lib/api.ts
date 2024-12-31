import { toast } from 'react-hot-toast';

const API_BASE_URL = 'http://localhost:5500/api';

async function checkServerConnection(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/analytics`);
    return response.ok;
  } catch {
    return false;
  }
}

export async function processDataFile(formData: FormData, p0: (progress: number) => void) {
  try {
    const isServerRunning = await checkServerConnection();
    if (!isServerRunning) {
      throw new Error('Backend server is not running. Please start the Flask server.');
    }

    const response = await fetch(`${API_BASE_URL}/process-data`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to process data');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Failed to connect to server';
    toast.error(message);
    throw error;
  }
}

export async function fetchAnalytics() {
  try {
    const isServerRunning = await checkServerConnection();
    if (!isServerRunning) {
      return {
        metrics: {
          total_sales: 0,
          total_profit: 0,
          average_order_value: 0,
          total_orders: 0,
          total_products: 0
        },
        category_analysis: {},
        layout_recommendations: {}
      };
    }

    const response = await fetch(`${API_BASE_URL}/analytics`);
    if (!response.ok) {
      throw new Error('Failed to fetch analytics data');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Analytics error:', error);
    return {
      metrics: {
        total_sales: 0,
        total_profit: 0,
        average_order_value: 0,
        total_orders: 0,
        total_products: 0
      },
      category_analysis: {},
      layout_recommendations: {}
    };
  }
}