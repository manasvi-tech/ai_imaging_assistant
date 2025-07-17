// src/components/Navbar.jsx
import { useNavigate } from 'react-router-dom';
import logo from '../assets/stethoscope.png';

const Navbar = () => {
    const navigate = useNavigate();
    const isLoggedIn = localStorage.getItem("token");

    const handleProtectedClick = (path) => {
        if (!isLoggedIn) {
            navigate('/login');
        } else {
            navigate(path);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <nav className="bg-[#206f6a] border-gray-200 py-6">
            <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto px-4">
                <a href="/" className="flex items-center space-x-3 rtl:space-x-reverse">
                    <img src={logo} className="h-9" alt="MediVision Logo" />
                    <span className="self-center text-2xl font-semibold whitespace-nowrap text-white">MediVision</span>
                </a>
                <button data-collapse-toggle="navbar-default" type="button" className="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-default" aria-expanded="false">
                    <span className="sr-only">Open main menu</span>
                    <svg className="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
                        <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 1h15M1 7h15M1 13h15" />
                    </svg>
                </button>
                <div className="hidden w-full md:block md:w-auto" id="navbar-default">
                    <ul className="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 bg-[#206f6a]">

                        <li>
                            <a href="/" className="block py-2 px-3 text-white hover:text-blue-300 md:p-0">Home</a>
                        </li>

                        <li>
                            <button onClick={() => handleProtectedClick('/dashboard')} className="block py-2 px-3 text-white hover:text-blue-300 md:p-0">
                                Dashbord
                            </button>
                        </li>

                        <li>
                            <button onClick={() => handleProtectedClick('/profile')} className="block py-2 px-3 text-white hover:text-blue-300 md:p-0">
                                Profile
                            </button>
                        </li>

                        {isLoggedIn && (
                            <li>
                                <a
                                    href="#"
                                    onClick={handleLogout}
                                    className="block py-2 px-3 text-red-400 hover:text-red-600 md:p-0"
                                >
                                    Logout
                                </a>
                            </li>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
