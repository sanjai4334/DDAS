import React from 'react';

const DownloadOptionsModal = ({ isOpen, onDownloadAgain, onReceiveFromDevice, onClose }) => {
    if (!isOpen) return null; // Don't render anything if modal is not open

    return (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50">
            <div className="bg-white rounded-lg shadow-lg p-6 max-w-sm w-full">
                <h2 className="text-xl font-bold mb-4">Download Options</h2>
                <p className="mb-6">Would you like to download the file again or receive it from another device?</p>
                <div className="flex justify-between">
                    <button
                        onClick={onDownloadAgain}
                        className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-full"
                    >
                        Download Again
                    </button>
                    <button
                        onClick={onReceiveFromDevice}
                        className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-full"
                    >
                        Receive from Device
                    </button>
                </div>
                <button
                    onClick={onClose}
                    className="mt-4 w-full bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-full"
                >
                    Cancel
                </button>
            </div>
        </div>
    );
};

export default DownloadOptionsModal;
