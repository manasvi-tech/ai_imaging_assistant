// import React, { useState, useEffect } from 'react';
// import axios from 'axios';
// import { useParams, useNavigate } from 'react-router-dom';
// import { useAuth } from '../contexts/AuthContext';
// import { FiEdit, FiEye, FiSave, FiZoomIn, FiZoomOut, FiRotateCw } from 'react-icons/fi';

// const ReportDashboard = () => {
//   const { reportId } = useParams();
//   const { user } = useAuth();
//   const navigate = useNavigate();
  
//   // State for the report data
//   const [report, setReport] = useState(null);
//   const [scan, setScan] = useState(null);
//   const [patient, setPatient] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState('');
  
//   // State for the report editor
//   const [isEditing, setIsEditing] = useState(false);
//   const [reportContent, setReportContent] = useState('');
  
//   // State for image viewer
//   const [zoomLevel, setZoomLevel] = useState(1);
//   const [rotation, setRotation] = useState(0);
  
//   // Check if user has edit permissions
//   const canEdit = user && (user.role === 'admin' || user.role === 'instructor');

//   useEffect(() => {
//     const fetchReportData = async () => {
//       try {
//         setLoading(true);
        
//         // Fetch report data
//         const reportRes = await axios.get(`http://localhost:8000/api/v1/reports/${reportId}`, {
//           headers: {
//             Authorization: `Bearer ${localStorage.getItem('token')}`
//           }
//         });
        
//         setReport(reportRes.data);
//         setReportContent(reportRes.data.content || '');
        
//         // Fetch scan data
//         const scanRes = await axios.get(`http://localhost:8000/api/v1/scans/${reportRes.data.scan_id}`, {
//           headers: {
//             Authorization: `Bearer ${localStorage.getItem('token')}`
//           }
//         });
        
//         setScan(scanRes.data);
        
//         // Fetch patient data
//         const patientRes = await axios.get(`http://localhost:8000/api/v1/patients/${scanRes.data.patient_id}`, {
//           headers: {
//             Authorization: `Bearer ${localStorage.getItem('token')}`
//           }
//         });
        
//         setPatient(patientRes.data);
        
//       } catch (err) {
//         console.error('Error fetching report data:', err);
//         setError(err.response?.data?.detail || 'Failed to load report data');
//       } finally {
//         setLoading(false);
//       }
//     };
    
//     fetchReportData();
//   }, [reportId]);

//   const handleSaveReport = async () => {
//     try {
//       const response = await axios.put(
//         `http://localhost:8000/api/v1/reports/${reportId}`,
//         { content: reportContent },
//         {
//           headers: {
//             Authorization: `Bearer ${localStorage.getItem('token')}`,
//             'Content-Type': 'application/json'
//           }
//         }
//       );
      
//       setReport(response.data);
//       setIsEditing(false);
//       // Show success message
//     } catch (err) {
//       console.error('Error saving report:', err);
//       setError(err.response?.data?.detail || 'Failed to save report');
//     }
//   };

//   if (loading) return <div className="text-center py-8">Loading report...</div>;
//   if (error) return <div className="text-center py-8 text-red-600">{error}</div>;
//   if (!report || !scan || !patient) return <div className="text-center py-8">Report data not found</div>;

//   return (
//     <div className="flex flex-col h-screen bg-gray-50">
//       {/* Header */}
//       <div className="bg-white border-b p-4 shadow-sm">
//         <h1 className="text-xl font-semibold">
//           Patient: {patient.name} (ID: {patient.medical_record_num || 'N/A'}) | 
//           Scan: {scan.scan_type} | 
//           Date: {new Date(scan.created_at).toLocaleDateString()}
//         </h1>
//       </div>
      
//       {/* Main Content */}
//       <div className="flex flex-1 overflow-hidden">
//         {/* Left Panel - Scan Viewer */}
//         <div className="flex-1 border-r p-4 bg-white overflow-auto">
//           <div className="flex justify-between items-center mb-4">
//             <h2 className="text-lg font-medium">SCAN VIEWER</h2>
//             <div className="flex space-x-2">
//               <button 
//                 onClick={() => setZoomLevel(zoom => Math.min(zoom + 0.1, 3))}
//                 className="p-2 rounded hover:bg-gray-100"
//                 title="Zoom In"
//               >
//                 <FiZoomIn />
//               </button>
//               <button 
//                 onClick={() => setZoomLevel(zoom => Math.max(zoom - 0.1, 0.5))}
//                 className="p-2 rounded hover:bg-gray-100"
//                 title="Zoom Out"
//               >
//                 <FiZoomOut />
//               </button>
//               <button 
//                 onClick={() => setRotation(rot => (rot + 90) % 360)}
//                 className="p-2 rounded hover:bg-gray-100"
//                 title="Rotate"
//               >
//                 <FiRotateCw />
//               </button>
//             </div>
//           </div>
          
//           <div className="flex justify-center items-center h-full">
//             {scan.file_path.endsWith('.dcm') ? (
//               <div className="bg-gray-200 p-8 rounded-lg text-center">
//                 <p>DICOM Viewer would be displayed here</p>
//                 <p className="text-sm text-gray-500">(Integration with DICOM viewer library needed)</p>
//               </div>
//             ) : (
//               <img 
//                 src={`file://${scan.file_path}`} 
//                 alt="Medical scan"
//                 style={{
//                   transform: `scale(${zoomLevel}) rotate(${rotation}deg)`,
//                   maxWidth: '100%',
//                   maxHeight: '80vh',
//                   objectFit: 'contain'
//                 }}
//                 onError={(e) => {
//                   e.target.onerror = null;
//                   e.target.src = '/placeholder-scan.png';
//                 }}
//               />
//             )}
//           </div>
//         </div>
        
//         {/* Right Panel - Report Editor */}
//         <div className="flex-1 p-4 bg-white overflow-auto">
//           <div className="flex justify-between items-center mb-4">
//             <h2 className="text-lg font-medium">REPORT EDITOR</h2>
//             {canEdit && (
//               <div className="flex space-x-2">
//                 {isEditing ? (
//                   <button
//                     onClick={handleSaveReport}
//                     className="flex items-center px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
//                   >
//                     <FiSave className="mr-1" /> Save
//                   </button>
//                 ) : (
//                   <button
//                     onClick={() => setIsEditing(true)}
//                     className="flex items-center px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
//                   >
//                     <FiEdit className="mr-1" /> Edit
//                   </button>
//                 )}
//                 <button
//                   onClick={() => setIsEditing(false)}
//                   className="flex items-center px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
//                 >
//                   <FiEye className="mr-1" /> View
//                 </button>
//               </div>
//             )}
//           </div>
          
//           {isEditing ? (
//             <textarea
//               value={reportContent}
//               onChange={(e) => setReportContent(e.target.value)}
//               className="w-full h-96 p-4 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
//               placeholder="Enter report findings..."
//             />
//           ) : (
//             <div className="prose max-w-none p-4 border rounded-md bg-gray-50">
//               <h3>Radiology Report</h3>
//               <p><strong>Patient:</strong> {patient.name}</p>
//               <p><strong>Scan Type:</strong> {scan.scan_type}</p>
//               <p><strong>Date:</strong> {new Date(scan.created_at).toLocaleDateString()}</p>
              
//               <div className="mt-4">
//                 <h4>Findings:</h4>
//                 {reportContent ? (
//                   <div dangerouslySetInnerHTML={{ __html: reportContent }} />
//                 ) : (
//                   <p className="text-gray-500">No findings recorded yet.</p>
//                 )}
//               </div>
              
//               <div className="mt-4">
//                 <h4>Impression:</h4>
//                 <p className="text-gray-500">[AI-generated impression would appear here]</p>
//               </div>
//             </div>
//           )}
          
//           {/* Placeholder for future AI integration */}
//           {canEdit && (
//             <div className="mt-6 p-4 border rounded-md bg-blue-50">
//               <h4 className="font-medium text-blue-800">AI Tools (Coming Soon)</h4>
//               <div className="flex space-x-4 mt-2">
//                 <button 
//                   className="px-3 py-1 bg-blue-100 text-blue-800 rounded hover:bg-blue-200"
//                   disabled
//                   title="Not yet implemented"
//                 >
//                   Analyze Scan
//                 </button>
//                 <button 
//                   className="px-3 py-1 bg-blue-100 text-blue-800 rounded hover:bg-blue-200"
//                   disabled
//                   title="Not yet implemented"
//                 >
//                   Segment Findings
//                 </button>
//               </div>
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ReportDashboard;



import React from 'react';
import { FiEdit, FiEye, FiSave, FiZoomIn, FiZoomOut, FiRotateCw } from 'react-icons/fi';

const ReportDashboardSkeleton = () => {
  // Hardcoded placeholder data
  const patient = {
    name: "John Doe",
    medical_record_num: "MRN123",
  };
  
  const scan = {
    scan_type: "MRI Brain",
    date: "Jan 15, 2024",
    file_type: "dcm" // or "png" for testing
  };
  
  const reportContent = `
    <p><strong>Findings:</strong></p>
    <ul>
      <li>Right frontal lobe lesion measuring 1.2cm</li>
      <li>Mild ventricular enlargement</li>
    </ul>
    <p><strong>Impression:</strong></p>
    <p>Suspicious for neoplastic process, recommend contrast-enhanced follow-up.</p>
  `;
  
  const canEdit = true; // Toggle this to test different permission states

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b p-4 shadow-sm">
        <h1 className="text-xl font-semibold">
          Patient: {patient.name} (ID: {patient.medical_record_num}) | 
          Scan: {scan.scan_type} | 
          Date: {scan.date}
        </h1>
      </div>
      
      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Panel - Scan Viewer */}
        <div className="flex-1 border-r p-4 bg-white overflow-auto">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium">SCAN VIEWER</h2>
            <div className="flex space-x-2">
              <button className="p-2 rounded hover:bg-gray-100">
                <FiZoomIn />
              </button>
              <button className="p-2 rounded hover:bg-gray-100">
                <FiZoomOut />
              </button>
              <button className="p-2 rounded hover:bg-gray-100">
                <FiRotateCw />
              </button>
            </div>
          </div>
          
          <div className="flex justify-center items-center h-full bg-gray-100 rounded-lg">
            {scan.file_type === 'dcm' ? (
              <div className="text-center p-8">
                <p className="mb-2">DICOM VIEWER PLACEHOLDER</p>
                <p className="text-sm text-gray-500">(Actual DICOM viewer would render here)</p>
              </div>
            ) : (
              <div className="text-center p-8">
                <p className="mb-2">SCAN IMAGE PREVIEW</p>
                <p className="text-sm text-gray-500">(Would show PNG/JPG/NIfTI images here)</p>
              </div>
            )}
          </div>
        </div>
        
        {/* Right Panel - Report Editor */}
        <div className="flex-1 p-4 bg-white overflow-auto">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium">REPORT EDITOR</h2>
            {canEdit && (
              <div className="flex space-x-2">
                <button className="flex items-center px-3 py-1 bg-blue-600 text-white rounded">
                  <FiEdit className="mr-1" /> Edit
                </button>
                <button className="flex items-center px-3 py-1 bg-gray-200 rounded">
                  <FiEye className="mr-1" /> View
                </button>
              </div>
            )}
          </div>
          
          {/* Report Content - Static for now */}
          <div className="prose max-w-none p-4 border rounded-md bg-gray-50">
            <h3>Radiology Report</h3>
            <p><strong>Patient:</strong> {patient.name}</p>
            <p><strong>Scan Type:</strong> {scan.scan_type}</p>
            <p><strong>Date:</strong> {scan.date}</p>
            
            <div dangerouslySetInnerHTML={{ __html: reportContent }} />
            
            <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded">
              <p className="text-yellow-800">[AI-generated content would appear here]</p>
            </div>
          </div>
          
          {/* Placeholder for AI tools */}
          {canEdit && (
            <div className="mt-6 p-4 border rounded-md bg-blue-50">
              <h4 className="font-medium text-blue-800">AI Tools (Coming Soon)</h4>
              <div className="flex space-x-4 mt-2">
                <button className="px-3 py-1 bg-blue-100 text-blue-800 rounded">
                  Analyze Scan
                </button>
                <button className="px-3 py-1 bg-blue-100 text-blue-800 rounded">
                  Segment Findings
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ReportDashboardSkeleton;