'use client';

import { useState } from 'react';

export default function ImageUploader() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [resultImage, setResultImage] = useState(null);
  const [count, setCount] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleUpload = async () => {
    if (!image) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', image);
    
    try {
      const response = await fetch('http://localhost:8000/process-image', {
        method: 'POST',
        body: formData,
      });
  
      const data = await response.json();
      setResultImage(`data:image/jpeg;base64,${data.processedImage}`);
      setCount(data.count);
    } catch (error) {
      console.error('Error uploading image:', error);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center space-y-4 p-4">
      <input type="file" accept="image/*" onChange={handleImageChange} className="mb-2" />
      {preview && <img src={preview} alt="Preview" className="w-64 h-auto rounded-lg" />}
      <button
        onClick={handleUpload}
        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        disabled={loading}
      >
        {loading ? 'Processing...' : 'Upload & Process'}
      </button>
      {resultImage && (
        <div className="text-center">
          <img src={resultImage} alt="Processed" className="w-64 h-auto rounded-lg mt-4" />
          <p className="mt-2 text-lg font-semibold">People Count: {count}</p>
        </div>
      )}
    </div>
  );
}
