import React from 'react';
import { FiPlay, FiPause, FiX } from 'react-icons/fi';

const ProgressBar = ({ fileName, progress, isPaused, handlePause, handleResume, handleCancel }) => {

    return (
        <div className="flex items-center justify-between mb-4">
            <div className="flex-grow">
                <p className="text-lg font-semibold">{fileName}</p>
                <div className="relative w-full h-1 bg-gray-200 rounded-full mt-2">
                    <div
                        className="absolute h-1 bg-green-500 rounded-full"
                        style={{ width: `${progress}%` }}
                    />
                </div>
                <p className="text-sm text-gray-600 mt-1">{progress}%</p>
            </div>
            <div className="flex items-center">
                <button
                    onClick={isPaused ? handleResume : handlePause}
                    className="flex items-center border-gray-400 text-gray-800 font-bold py-2 px-4 rounded mr-2"
                >
                    {isPaused ? <FiPlay /> : <FiPause />}
                </button>
                <button
                    onClick={handleCancel}
                    className="flex items-center border-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
                >
                    <FiX className="mr-2" />
                </button>
            </div>
        </div>
    );
};

export default ProgressBar;
