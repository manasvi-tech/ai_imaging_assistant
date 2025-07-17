import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ScanUploader = () => {
  const [patientName, setPatientName] = useState('');
  const [patientId, setPatientId] = useState('');
  const [scanType, setScanType] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [patientResults, setPatientResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  // Search patients when name changes (with debounce)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (patientName.length >= 2) {
        handlePatientSearch();
      } else {
        setPatientResults(res.data.patients || []);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [patientName]);

  const handlePatientSearch = async () => {
    try {
      setIsSearching(true);
      setError('');

      const res = await axios.get(`http://localhost:8000/api/v1/patients/search/`, {
        params: {
          name: patientName,
          skip: 0,
          limit: 10
        }
      });

      console.log('API Response:', res.data);

      if (Array.isArray(res.data)) {
        setPatientResults(res.data);
      } else {
        throw new Error('Unexpected response format');
      }
    } catch (err) {
      console.error('Search error:', err);
      setError(err.message);
      setPatientResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleUpload = async (e) => {
  e.preventDefault();
  setError('');
  setSuccess('');

  if (!file || !patientId || !scanType) {
    setError('Please select a patient, scan type, and file');
    return;
  }

  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('scan_type', scanType);
    formData.append('patient_id', patientId);

    // Update this line to match your backend endpoint
    await axios.post('http://localhost:8000/api/v1/scans/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });

    setSuccess('Scan uploaded successfully!');
    // Reset form
    setFile(null);
    setPatientName('');
    setPatientId('');
    setScanType('');
    setPatientResults([]);
  } catch (err) {
    console.error('Upload error:', err);
    setError(err.response?.data?.detail || 'Upload failed. Please try again.');
  }
};

  return (
    <div className="max-w-md mx-auto p-6 bg-white shadow-lg rounded-xl">
      <h2 className="text-2xl font-bold mb-4 text-[#206f6a]">Upload Scan</h2>

      <form onSubmit={handleUpload} className="space-y-4">
        <div>
          <label className="block font-medium text-gray-700 mb-1">
            Patient Search
          </label>
          <input
            type="text"
            value={patientName}
            onChange={(e) => setPatientName(e.target.value)}
            className="w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#206f6a]"
            placeholder="Start typing patient name..."
          />

          {isSearching && <p className="text-sm text-gray-500">Searching...</p>}

          {patientResults.length > 0 && (
            <div className="mt-2 border rounded-md max-h-40 overflow-y-auto">
              {patientResults.map(patient => (
                <div
                  key={patient.id}
                  className={`p-2 hover:bg-gray-100 cursor-pointer ${patientId === patient.id ? 'bg-blue-50' : ''}`}
                  onClick={() => {
                    setPatientId(patient.id);
                    setPatientName(patient.name);
                    setPatientResults([]);
                  }}
                >
                  {patient.name} {patient.medical_record_num && `(ID: ${patient.medical_record_num})`}
                </div>
              ))}
            </div>
          )}
        </div>

        <div>
          <label className="block font-medium text-gray-700 mb-1">
            Scan Type
          </label>
          <select
            value={scanType}
            onChange={(e) => setScanType(e.target.value)}
            className="w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#206f6a]"
            required
          >
            <option value="">Select scan type</option>
            <option value="CT">CT</option>
            <option value="X-ray">X-ray</option>
            <option value="MRI">MRI</option>
          </select>
        </div>

        <div>
          <label className="block font-medium text-gray-700 mb-1">
            Select File
          </label>
          <input
            type="file"
            accept=".dcm,.nii,.nii.gz,.png,.jpg"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="w-full border rounded-md px-3 py-2 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-[#206f6a] file:text-white file:cursor-pointer"
            required
          />
        </div>

        {error && <p className="text-red-600">{error}</p>}
        {success && <p className="text-green-600">{success}</p>}

        <button
          type="submit"
          className={`w-full bg-[#206f6a] hover:bg-[#1c5a56] text-white py-2 px-4 rounded-md transition ${!patientId || !scanType || !file ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          disabled={!patientId || !scanType || !file}
        >
          Upload Scan
        </button>
      </form>
    </div>
  );
};

export default ScanUploader;