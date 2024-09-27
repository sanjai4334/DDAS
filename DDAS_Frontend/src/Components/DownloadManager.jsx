// import React, { useState } from 'react';

// const DownloadManager = ({ handleStartDownload, handleClose, handleError }) => {
//     const [url, setUrl] = useState('');
//     const [error, setError] = useState('');

//     const validateUrl = (url) => {
//         try {
//             new URL(url);
//             return true;
//         } catch {
//             return false;
//         }
//     };

//     const handleStart = () => {
//         if (validateUrl(url)) {
//             handleStartDownload(url);
//             setError('');
//         } else {
//             setError('Please enter a valid URL.');
//             handleError(); // Trigger error notification
//         }
//     };

//     return (
//         <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6 my-4 relative">
//             <div className="flex justify-between items-center mb-4">
//                 <button onClick={handleClose} className="absolute top-2 right-2 text-gray-600 hover:text-gray-800">
//                     <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-6 h-6">
//                         <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
//                     </svg>
//                 </button>
//             </div>
//             <input
//                 type="text"
//                 value={url}
//                 onChange={(e) => setUrl(e.target.value)}
//                 placeholder="Paste URL here..."
//                 className="w-full p-2 border border-gray-300 rounded-lg"
//             />
//             {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
//             <button
//                 onClick={handleStart}
//                 className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-full mb-4 w-full mt-4"
//             >
//                 Start Download
//             </button>
//         </div>
//     );
// };

// export default DownloadManager;


import React, { useState } from 'react';
import NotificationProvider from './NotificationProvider';
import { useSnackbar } from 'notistack';
import DownloadOptionsModal from './DownloadOptionsModal'; // Import the new component

const DownloadManager = ({ handleStartDownload, handleClose, handleError }) => {
    const { enqueueSnackbar } = useSnackbar();
    const [url, setUrl] = useState('');
    const [error, setError] = useState('');
    const [isModalOpen, setModalOpen] = useState(false);

    const validateUrl = (url) => {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    };

    const handleStart = () => {
        if (validateUrl(url)) {
            // Trigger modal for options instead of direct download
            setModalOpen(true);
        } else {
            setError('Please enter a valid URL.');
            enqueueSnackbar('Enter valid URl!', { variant: 'info' });
            handleError();
        }
    };

    const handleDownloadAgain = () => {
        handleStartDownload(url);
        setModalOpen(false);
        enqueueSnackbar('Download starts!', { variant: 'success' });
    };

    const handleReceiveFromDevice = () => {
        // Logic for receiving from another device
        setModalOpen(false);
        enqueueSnackbar('Receiving from another device!', { variant: 'info' });
    };

    return (
        <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6 my-4 relative">
            <div className="flex justify-between items-center mb-4">
                <button onClick={handleClose} className="absolute top-2 right-2 text-gray-600 hover:text-gray-800">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-6 h-6">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Paste URL here..."
                className="w-full p-2 border border-gray-300 rounded-lg"
            />
            {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
            <button
                onClick={handleStart}
                className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-full mb-4 w-full mt-4"
            >
                Start Download
            </button>

            {/* Download Options Modal */}
            <DownloadOptionsModal
                isOpen={isModalOpen}
                onDownloadAgain={handleDownloadAgain}
                onReceiveFromDevice={handleReceiveFromDevice}
                onClose={() => setModalOpen(false)}
            />
        </div>
    );
};

export default function WrappedApp() {
    return (
        <NotificationProvider>
            <DownloadManager />
        </NotificationProvider>
    );
}