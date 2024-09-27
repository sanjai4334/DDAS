import React, { useState, useRef } from "react";
import { FiPlus, FiSearch } from "react-icons/fi";
import { useSnackbar } from 'notistack'; // Import useSnackbar hook
import DownloadManager from "./Components/DownloadManager";
import ProgressBar from "./Components/ProgressBar";
import NotificationProvider from "./Components/NotificationProvider"; // Import NotificationProvider

function App() {
  const [connections, setConnections] = useState(["File1", "File2"]);
  const [showDownloadControls, setShowDownloadControls] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [currentFileName, setCurrentFileName] = useState("");
  const { enqueueSnackbar } = useSnackbar(); // Access the enqueueSnackbar function
  const downloadIntervalRef = useRef(null); // Ref to hold the interval

  const handleAddClick = () => {
    setShowDownloadControls(true);
  };

  const handleCloseModal = () => {
    setShowDownloadControls(false);
  };

  const handleStartDownload = (url) => {
    setShowDownloadControls(false);
    setDownloading(true);
    setProgress(0);
    setIsPaused(false);
    setCurrentFileName(url);

    downloadIntervalRef.current = setInterval(() => {
      setProgress((oldProgress) => {
        if (oldProgress >= 100) {
          clearInterval(downloadIntervalRef.current);
          setDownloading(false);
          enqueueSnackbar('Download complete!', { variant: 'success' });
          return 100; // Cap the progress at 100%
        }
        if (!isPaused) {
          const newProgress = oldProgress + 2; // Smaller increment for smooth progress
          return newProgress >= 100 ? 100 : newProgress; // Ensure progress doesn't exceed 100
        }
        return oldProgress;
      });
    }, 100); // Faster updates with smaller increments
  };

  const handlePause = () => {
    setIsPaused(true);
  };

  const handleResume = () => {
    setIsPaused(false);
  };

  const handleCancel = () => {
    if (downloadIntervalRef.current) {
      clearInterval(downloadIntervalRef.current); // Clear the interval on cancel
    }
    setDownloading(false);
    setProgress(0);
    setCurrentFileName('');
    enqueueSnackbar('Download canceled!', { variant: 'warning' });
  };

  const handleError = () => {
    enqueueSnackbar('An error occurred during the download.', { variant: 'error' });
  };

  return (
    <div className="flex h-screen">
      <div className="w-64 bg-gray-100 h-full p-4 border-r">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">DataSets</h2>
          <FiPlus className="text-gray-500 cursor-pointer" onClick={handleAddClick} />
        </div>

        <h3 className="text-gray-600 mb-2">Search</h3>

        <div className="relative mb-4">
          <input
            type="text"
            placeholder="Search Files"
            className="w-full p-2 pl-10 border rounded-md focus:outline-none focus:ring focus:ring-blue-300"
          />
          <FiSearch className="absolute top-2 left-2 text-gray-400 mt-1" />
        </div>

        <ul>
          {connections.map((conn, index) => (
            <li
              key={index}
              className="flex items-center py-2 text-gray-700 hover:bg-gray-200 cursor-pointer rounded-md"
            >
              {conn}
            </li>
          ))}
        </ul>
      </div>

      <div className="flex-1 p-4">
        <h2 className="text-2xl font-bold mb-4">Download Progress</h2>
        {downloading ? (
          <ProgressBar
            fileName={currentFileName.split('/').pop()}
            progress={progress}
            isPaused={isPaused}
            handlePause={handlePause}
            handleResume={handleResume}
            handleCancel={handleCancel}
          />
        ) : (
          <p className="text-gray-500">No active downloads.</p>
        )}
      </div>

      {showDownloadControls && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-10">
          <DownloadManager
            handleStartDownload={handleStartDownload}
            handleClose={handleCloseModal}
            handleError={handleError}
          />
        </div>
      )}
    </div>
  );
}

export default function WrappedApp() {
  return (
    <NotificationProvider>
      <App />
    </NotificationProvider>
  );
}
