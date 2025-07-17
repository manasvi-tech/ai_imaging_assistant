import React from 'react';
import walpaper from '../assets/homepage/copy-space-stethoscope-medicine.jpg';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react'; // Or use a custom SVG if you prefer

const Home = () => {
  return (
    <div className="w-full min-h-screen">


      {/* Hero Section */}
      <section className="w-full h-screen relative">
        <img src={walpaper} alt="Medical Hero" className="w-full h-full object-cover opacity-90" />
        <div className="absolute inset-0 flex flex-col justify-center items-start text-white px-8 md:px-20 font-serif">
          <h1 className="text-8xl font-bold text-[#206f6a] mb-4 mt-[-2rem]" style={{ fontFamily: "Roboto Slab" }}>MediVision</h1>
          <p className="text-2xl md:text-2xl font-light max-w-xl text-[#206f6a]">
            Clarity in every scan.<br />
            Empowering radiologists and clinicians with instant image insights and automated reporting
          </p>

          <Link
            to="/login"
            className="inline-flex items-center gap-2 bg-[#206f6a] text-white px-6 py-3 rounded-full text-lg font-semibold shadow-md hover:bg-[#1a5d58] transition-all duration-300 my-6"
          >
            Get Started
            <ArrowRight size={20} />
          </Link>


        </div>
      </section>

      {/* Features Section */}
      <section className="bg-white text-gray-800 py-20 px-6 md:px-20">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold mb-12 text-center text-teal-600">Why Choose MediVision</h3>
          <div className='flex gap-20'>
            <div className="mb-12">
              <h4 className="text-2xl font-semibold text-teal-600" style={{textAlign:"center"}}>AI-Powered Image Analysis</h4>
              <p className="mt-2 text-lg" style={{textAlign:"center"}}>
                Upload DICOM, PNG, or JPEG scans and let MediVision instantly segment and interpret the images with deep-learning models and expert-tuned algorithms.
              </p>
            </div>

            <div className="mb-12">
              <h4 className="text-2xl font-semibold text-teal-600" style={{textAlign:"center"}}>Smart Report Generation</h4>
              <p className="mt-2 text-lg" style={{textAlign:"center"}}>
                Automatically draft preliminary radiology reports using multimodal reasoning from both image and clinical context. Review and edit with ease.
              </p>
            </div>

            <div>
              <h4 className="text-2xl font-semibold text-teal-600" style={{textAlign:"center"}}>Seamless Patient Workflow</h4>
              <p className="mt-2 text-lg align" style={{textAlign:"center"}}>
                From patient registration to scan upload and diagnosis generation, streamline your entire diagnostic process—secured with authentication and role-based access.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
