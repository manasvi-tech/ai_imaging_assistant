import { useEffect, useState } from 'react';
import axios from '../api/axios';
import ScanUploader from '../components/ScanUploader';
import PatientForm from '../components/PatientForm';

export default function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    axios.get('/auth/me').then(res => setProfile(res.data));
    axios.get('/patients').then(res => setPatients(res.data));
  }, []);

  return (


    <div className='flex'>
      <div className="w-[25%] h-screen left-0 top-0 bg-[#206f6a] text-white border-t-2 flex flex-col">
        <PatientForm />
        <div className="px-6 font-sans mt-5">
          <h3 className="font-bold pt-8 " style={{ justifyContent: "center", display: "flex" }}>Recent Patients</h3>
          <hr className='my-7' />
          <ul className="space-y-2">
            {patients
              .sort((a, b) => b.id - a.id) // Sort by highest ID first (assuming newer patients have higher IDs)
              .slice(0, 2) // Take only first 2
              .map(patient => (
                <li key={patient.id} className="p-2 hover:bg-[#1a5f5a] rounded cursor-pointer">
                  {patient.name} (ID: {patient.medical_record_num})
                </li>
              ))}
          </ul>
        </div>
      </div>
      <div className='flex-1 p-4'> {/* Added flex-1 and padding */}
        <div className="border-b border-gray-200 pb-2 mb-4">
          <h2 className="font-roboto-slab text-4xl text-[#206f6a]" style={{ textAlign: "center" }}  >
            Radiology Report
          </h2>
          <hr className='my-4 text-[#206f6a]' />
          <ScanUploader />
        </div>
      </div>

    </div>


  );
}
