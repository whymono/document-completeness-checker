import React, { useState, useCallback } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";
import { motion } from "framer-motion";

const UploadCard = ({ setAnalysisResult, isBackendReachable }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const apiurl = import.meta.env.VITE_API_URL

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      handleUpload(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: "application/pdf",
    multiple: false,
  });

  const handleUpload = async (fileToUpload) => {
    if (!fileToUpload) {
      setError("Please select a file to upload.");
      return;
    }

    setUploading(true);
    setError(null);
    setAnalysisResult(null);

    const formData = new FormData();
    formData.append("file", fileToUpload);

    try {
      const response = await axios.post(`${apiurl}/upload-pdf`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setAnalysisResult(response.data);
    } catch (error) {
      setError(error.response ? error.response.data.detail : "An error occurred while uploading the file.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <motion.div
      {...getRootProps()}
      className={`upload-card ${isDragActive ? "drag-active" : ""}`}
      whileHover={{ scale: 1.02 }}
    >
      <input {...getInputProps()} />
      {uploading ? (
        <>
          <div className="loader"></div>
          <p>Analyzing your document...</p>
        </>
      ) : (
        <>
          <p className="upload-icon">📄</p>
          <h1>{isDragActive ? "Drop it like it's hot!" : "Drag & drop your PDF here"}</h1>
          <p>or click to select a file</p>
          {file && <p className="file-name">Selected file: {file.name}</p>}
        </>
      )}
      {error && <p className="error">{error}</p>}
    </motion.div>
  );
};

export default UploadCard;
