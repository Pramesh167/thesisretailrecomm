import React, { useState, useEffect } from 'react';
import { Upload } from 'lucide-react';
import { processDataFile } from '../lib/api';
import { toast } from 'react-hot-toast';

interface FileUploadProps {
  onUploadComplete?: () => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadComplete }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<string | null>(null);

  const allowedExtensions = ['.xlsx', '.xls', '.csv', '.txt'];

  const isValidFileType = (filename: string): boolean => {
    const ext = filename.toLowerCase().slice((filename.lastIndexOf(".") - 1 >>> 0) + 2);
    return allowedExtensions.includes(`.${ext}`);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    setError(null);

    const file = e.dataTransfer.files[0];
    if (file && isValidFileType(file.name)) {
      await processFile(file);
    } else {
      setError('Invalid file type. Please upload an Excel, CSV, or TXT file.');
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (isValidFileType(file.name)) {
        await processFile(file);
      } else {
        setError('Invalid file type. Please upload an Excel, CSV, or TXT file.');
      }
    }
  };

  const processFile = async (file: File) => {
    setIsUploading(true);
    setProgress('Uploading file...');
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      await processDataFile(formData, (progress) => {
        setProgress(`Uploading file... ${progress}%`);
      });
      toast.success('Data processed successfully!');
      setProgress('Data processed successfully!');
      onUploadComplete?.();
      
      setTimeout(() => {
        setProgress(null);
        setIsUploading(false);
      }, 2000);
        
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error processing file. Please try again.';
      setError(message);
      setIsUploading(false);
      setProgress(null);
    }
  };

  return (
    <div className="max-w-xl mx-auto">
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center ${
          isDragging ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <Upload className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">
          Upload your retail store dataset
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Supported formats: Excel (.xlsx, .xls), CSV, TXT
        </p>
        <div className="mt-4">
          <label className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 cursor-pointer">
            Browse Files
            <input
              type="file"
              className="hidden"
              accept=".xlsx,.xls,.csv,.txt"
              onChange={handleFileSelect}
              disabled={isUploading}
            />
          </label>
        </div>
        {progress && (
          <div className="mt-4 text-sm text-indigo-600">{progress}</div>
        )}
        {error && (
          <div className="mt-4 text-sm text-red-600">{error}</div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;