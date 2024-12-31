import { createClient } from '@supabase/supabase-js';
import { config, validateConfig } from './config';

// Validate configuration before creating client
validateConfig();

export const supabase = createClient(
  config.supabase.url,
  config.supabase.anonKey
);