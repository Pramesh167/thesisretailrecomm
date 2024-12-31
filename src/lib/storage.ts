import { supabase } from './supabase';

export async function uploadDataFile(file: File) {
  const { data, error } = await supabase.storage
    .from('retail-data')
    .upload(`uploads/${file.name}`, file);

  if (error) throw error;
  return data;
}

export async function getFileUrl(path: string) {
  const { data } = await supabase.storage
    .from('retail-data')
    .getPublicUrl(path);
  
  return data.publicUrl;
}