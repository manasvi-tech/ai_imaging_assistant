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
        
      </div>
      <div className='flex-1 p-4'> {/* Added flex-1 and padding */}
        <div className="border-b border-gray-200 pb-2 mb-4">
          <h2 className="font-roboto-slab text-4xl text-[#206f6a]" style={{ textAlign: "center" }}  >
            Medical Imaging Assistant
          </h2>
          <hr className='my-4 text-[#206f6a]' />
          <ScanUploader />
        </div>
      </div>

    </div>


  );
}
