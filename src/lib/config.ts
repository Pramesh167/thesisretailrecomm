// Environment configuration
export const config = {
  supabase: {
    url: import.meta.env.VITE_SUPABASE_URL,
    anonKey: import.meta.env.VITE_SUPABASE_ANON_KEY,
  },
} as const;

// Validation function
export function validateConfig() {
  if (!config.supabase.url || !config.supabase.anonKey) {
    throw new Error(
      'Missing Supabase configuration. Please click the "Connect to Supabase" button in the top right to set up your project.'
    );
  }
}