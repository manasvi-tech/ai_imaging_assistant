import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const PatientForm = () => {
    const navigate = useNavigate();
    const [patient, setPatient] = useState({
        name: '',
        age: '',
        sex: 'Male',
        medical_record_num: ''  // Changed from patientId to match your backend
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setPatient(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setIsLoading(true);

        try {
            // Validate required fields
            if (!patient.name || !patient.medical_record_num) {
                throw new Error('Name and Medical Record Number are required');
            }

            const response = await axios.post('http://localhost:8000/api/v1/patients/', 
                patient,
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                }
            );

            setSuccess('Patient created successfully!');
            // Reset form after successful submission
            setPatient({
                name: '',
                age: '',
                sex: 'Male',
                medical_record_num: ''
            });
            
            // Optionally redirect after a delay
            setTimeout(() => {
                navigate('/dashboard'); // Assuming you have a patients list route
            }, 1500);

        } catch (err) {
            console.error('Error creating patient:', err);
            if (err.response) {
                // Backend returned an error response
                setError(err.response.data.detail || 'Failed to create patient');
            } else if (err.request) {
                // No response received
                setError('No response from server. Please try again.');
            } else {
                // Other errors
                setError(err.message || 'Failed to create patient');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="px-6 pt-10 font-sans mt-5">
            {/* Title */}
            <h3 className="text-lg font-semibold text-white my-3 text-center">Add New Patient</h3>
            <hr className='my-8'/>
            
            {/* Success message */}
            {success && (
                <div className="mb-4 p-2 bg-green-100 text-green-700 rounded">
                    {success}
                </div>
            )}
            
            {/* Error message */}
            {error && (
                <div className="mb-4 p-2 bg-red-100 text-red-700 rounded">
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-2 mx-3">
                {/* Patient Name */}
                <div className="space-y-0.5">
                    <label className="block text-sm font-medium text-white">Patient Name*</label>
                    <input
                        type="text"
                        name="name"
                        value={patient.name}
                        onChange={handleChange}
                        className="w-full p-1 text border border-gray-300 rounded text-sm text-black"
                        placeholder="John Doe"
                        required
                    />
                </div>

                {/* Age and Sex - Horizontal layout */}
                <div className="flex space-x-2">
                    <div className="flex-1 space-y-0.5">
                        <label className="block text-sm font-medium text-white">Age</label>
                        <input
                            type="number"
                            name="age"
                            value={patient.age}
                            onChange={handleChange}
                            className="w-full p-1 border border-gray-300 rounded text-sm text-black"
                            placeholder="40"
                            min="0"
                            max="120"
                        />
                    </div>
                    <div className="flex-1 space-y-0.5">
                        <label className="block text-sm font-medium text-white">Sex</label>
                        <select
                            name="sex"
                            value={patient.sex}
                            onChange={handleChange}
                            className="w-full p-1 border border-gray-300 rounded text-sm text-black"
                        >
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                </div>

                {/* Medical Record Number */}
                <div className="space-y-0.5">
                    <label className="block text-sm font-medium text-white">Medical Record Number*</label>
                    <input
                        type="text"
                        name="medical_record_num"
                        value={patient.medical_record_num}
                        onChange={handleChange}
                        className="w-full p-1 border border-gray-300 rounded text-sm text-black"
                        placeholder="MRN12345"
                        required
                    />
                </div>

                {/* Submit Button */}
                <button 
                    type="submit" 
                    className={`w-full mt-4 py-1 px-4 bg-teal-500 text-white rounded-md 
                                hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500
                                ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                    disabled={isLoading}
                >
                    {isLoading ? 'Creating...' : '+ Add Patient'}
                </button>
            </form>
        </div>
    );
};

export default PatientForm;