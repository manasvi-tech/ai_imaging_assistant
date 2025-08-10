import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import image from '../assets/homepage/image.jpg'

const ReportDashboard = () => {
  const { reportId } = useParams();
  const { user, loading: authLoading } = useAuth();
  const [report, setReport] = useState(null);
  const [scanImage, setScanImage] = useState(null);
  const [doctorNotes, setDoctorNotes] = useState('');
  const [finalReport, setFinalReport] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [error, setError] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [imageError, setImageError] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [success, setSuccess] = useState('');
  const [segmentedImage, setSegmentedImage] = useState(null);
  const [isGeneratingSegmented, setIsGeneratingSegmented] = useState(false);

  const canEdit = ['instructor', 'admin'].includes(user?.role);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchReportData = async () => {
      try {
        setIsLoading(true);
        const response = await axios.get(
          `http://localhost:8000/api/v1/reports/${reportId}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );
        const data = response.data;
        setReport(data);
        setDoctorNotes(data.doctor_notes || '');
        setFinalReport(data.final_report || data.generated_diagnosis || '');

        if (data.scan_id) {
          await fetchScanImage(data.scan_id);
        }
      } catch (err) {
        console.error('Error fetching report:', err);
        setError('Failed to load report');
      } finally {
        setIsLoading(false);
      }
    };

    const fetchScanImage = async (scanId) => {
      try {
        setImageError('');
        const response = await axios.get(
          `http://localhost:8000/api/v1/scans/${scanId}/image`,
          {
            responseType: 'blob',
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );

        // Check if the response is actually an image
        if (!response.data.type.startsWith('image/')) {
          throw new Error('Unsupported file format');
        }

        const imageUrl = URL.createObjectURL(response.data);
        setScanImage(imageUrl);
      } catch (err) {
        console.error('Error fetching scan image:', err);
        setImageError('Could not display scan image. The file may be in an unsupported format.');
        setScanImage(null);
      }
    };

    fetchReportData();

    return () => {
      if (scanImage) {
        URL.revokeObjectURL(scanImage);
      }
      if (segmentedImage) {
        URL.revokeObjectURL(segmentedImage);
      }
    };
  }, [reportId]);

  const handleSaveReport = async () => {
    try {
      console.log('User Role:', user?.role);
      const response = await axios.put(
        `http://localhost:8000/api/v1/reports/${reportId}`,
        {
          doctor_notes: doctorNotes,
          final_report: finalReport,
          generated_diagnosis: canEdit ? finalReport : report.generated_diagnosis
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        }
      );

      setReport(response.data);
      setDoctorNotes(response.data.doctor_notes || '');
      setFinalReport(response.data.final_report || '');
      setIsEditing(false);
      setError('');
      setSuccess('Report saved successfully!');
      
    } catch (err) {
      console.error('Error saving report:', err);
      setError(err.response?.data?.detail || 'Failed to save report');
    }
  };

  const handleGenerateSegmentedImage = () => {
    setIsGeneratingSegmented(true);
    // Replace this path with your actual segmented image path
    const segmentedImagePath = image
    
    // Simulate a brief loading time
    setTimeout(() => {
      setSegmentedImage(segmentedImagePath);
      setIsGeneratingSegmented(false);
    }, 500);
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
    if (isExpanded) {
      setZoomLevel(1);
    }
  };

  const handleZoom = (direction) => {
    setZoomLevel(prev => {
      const newZoom = direction === 'in' ? prev + 0.1 : prev - 0.1;
      return Math.max(0.5, Math.min(newZoom, 3));
    });
  };

  if (authLoading) {
    return <div className="p-4">Loading user authentication...</div>;
  }

  if (isLoading) {
    return <div className="p-4">Loading report...</div>;
  }

  if (!report) {
    return <div className="p-4 text-red-500">{error || 'Report not found'}</div>;
  }



  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Report Dashboard</h1>

      {error && <p className="text-red-500 mb-4">{error}</p>}
      {success && (
        <div className="p-2 mb-4 text-green-700 bg-green-100 rounded">
          {success}
        </div>
      )}
      <div className="flex flex-col md:flex-row gap-6">
        {/* Modified Scan Viewer - Left Side */}
        <div className={`${isExpanded ? 'fixed inset-0 z-50 bg-black bg-opacity-90 flex items-center justify-center' : 'w-full md:w-1/2'} relative`}>
          {/* Controls - Now at top right */}
          <div className={`absolute ${isExpanded ? 'top-4 right-4' : 'top-2 right-2'} z-10 flex space-x-2 bg-white bg-opacity-50 rounded-full p-1`}>
            <button
              onClick={() => handleZoom('in')}
              className="p-2 rounded-full hover:bg-gray-200"
              disabled={zoomLevel >= 3}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
            </button>
            <button
              onClick={() => handleZoom('out')}
              className="p-2 rounded-full hover:bg-gray-200"
              disabled={zoomLevel <= 0.5}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
            </button>
            <button
              onClick={toggleExpand}
              className="p-2 rounded-full hover:bg-gray-200"
            >
              {isExpanded ? (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M3 4a1 1 0 011-1h4a1 1 0 010 2H6.414l2.293 2.293a1 1 0 01-1.414 1.414L5 6.414V8a1 1 0 01-2 0V4zm9 1a1 1 0 010-2h4a1 1 0 011 1v4a1 1 0 01-2 0V6.414l-2.293 2.293a1 1 0 11-1.414-1.414L13.586 5H12zm-9 7a1 1 0 012 0v1.586l2.293-2.293a1 1 0 111.414 1.414L6.414 15H8a1 1 0 010 2H4a1 1 0 01-1-1v-4zm13-1a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 010-2h1.586l-2.293-2.293a1 1 0 111.414-1.414L15 13.586V12a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
              )}
            </button>
          </div>

          {/* Left Side Content */}
          <div className={`${isExpanded ? 'hidden' : 'w-full'}`}>
            {/* Image Display - Now with proper containment */}
            {scanImage ? (
              <div className="h-96 flex items-center justify-center overflow-hidden">
                <img
                  src={scanImage}
                  alt="Medical scan"
                  className="max-h-full max-w-full object-contain"
                  style={{ transform: `scale(${zoomLevel})` }}
                />
              </div>
            ) : (
              <div className="bg-gray-100 h-96 flex items-center justify-center rounded-lg">
                {imageError ? (
                  <div className="text-center p-4">
                    <p className="text-red-500 mb-2">{imageError}</p>
                    <p className="text-sm text-gray-500">Supported formats: DICOM, NIfTI, PNG, JPG</p>
                  </div>
                ) : (
                  <p className="text-gray-500">No scan image available</p>
                )}
              </div>
            )}

            {/* Generate Segmented Image Button */}
            <div className="mt-4">
              <button
                onClick={handleGenerateSegmentedImage}
                disabled={isGeneratingSegmented || !scanImage}
                className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white px-4 py-2 rounded transition-colors"
              >
                {isGeneratingSegmented ? 'Generating...' : 'Generate Segmented Image'}
              </button>
            </div>

            {/* Segmented Image Display */}
            {segmentedImage && (
              <div className="mt-4">
                <h3 className="text-lg font-semibold mb-2">Segmented Image</h3>
                <div className="h-96 flex items-center justify-center overflow-hidden rounded-lg border">
                  <img
                    src={segmentedImage}
                    alt="Segmented medical scan"
                    className="max-h-full max-w-full object-contain"
                    style={{ transform: `scale(${zoomLevel})` }}
                  />
                </div>
              </div>
            )}
          </div>

          {/* Expanded view content */}
          {isExpanded && (
            <div className="h-full w-full flex items-center justify-center">
              {scanImage && (
                <img
                  src={scanImage}
                  alt="Medical scan"
                  className="max-h-full max-w-full object-contain"
                  style={{ transform: `scale(${zoomLevel})` }}
                />
              )}
            </div>
          )}
        </div>

        {/* Right Side Content - Keep EXACTLY as it was before */}
        <div className={`${isExpanded ? 'hidden' : 'w-full md:w-1/2'}`}>
          <div className="bg-gray-100 p-4 rounded-md shadow-md">
            <h2 className="text-xl font-semibold mb-2">AI Diagnosis</h2>
            {isEditing ? (
              <textarea
                value={finalReport}
                onChange={(e) => setFinalReport(e.target.value)}
                className="w-full h-48 p-3 border rounded-md mb-4"
                disabled={!canEdit}
              />
            ) : (
              <p className="whitespace-pre-line text-gray-800 mb-4">
                {report?.generated_diagnosis || 'No AI diagnosis available.'}
              </p>
            )}

            {isEditing ? (
              <>
                <div className="mb-4">
                  <label className="block font-medium mb-1">Doctor Notes:</label>
                  <textarea
                    value={doctorNotes}
                    onChange={(e) => setDoctorNotes(e.target.value)}
                    className="w-full h-32 p-3 border rounded-md"
                  />
                </div>

                <div className="flex space-x-2">
                  <button
                    onClick={handleSaveReport}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                  >
                    Save
                  </button>
                  <button
                    onClick={() => setIsEditing(false)}
                    className="bg-gray-400 hover:bg-gray-500 text-white px-4 py-2 rounded"
                  >
                    Cancel
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="mb-4">
                  <h2 className="text-xl font-semibold mb-1">Doctor Notes</h2>
                  <p className="whitespace-pre-line text-gray-700">
                    {doctorNotes || 'No notes yet.'}
                  </p>
                </div>

                <button
                  onClick={() => setIsEditing(true)}
                  className={`bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded ${!canEdit ? 'opacity-50 cursor-not-allowed' : ''}`}
                  disabled={!canEdit}
                >
                  Edit Report
                </button>
                {!canEdit && (
                  <p className="text-sm text-gray-500 mt-2">
                    Only instructors and administrators can edit reports.
                  </p>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportDashboard;