import React, { useState, useCallback } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";

const UploadCard = ({ setAnalysisResult }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const apiurl = import.meta.env.VITE_API_URL

  const handleUpload = useCallback(async (fileToUpload) => {
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
      
      const jobId = response.data.job_id;
      let isCompleted = false;
      
      while (!isCompleted) {
        const statusResponse = await axios.get(`${apiurl}/job/${jobId}`);
        const data = statusResponse.data;
        
        if (data.status === "completed") {
          setAnalysisResult(data.result);
          isCompleted = true;
          setUploading(false);
        } else if (data.status === "failed") {
          setError(data.error || "Analysis failed.");
          isCompleted = true;
          setUploading(false);
        } else {
          // Wait for 2 seconds before polling again
          await new Promise((resolve) => setTimeout(resolve, 2000));
        }
      }
    } catch (error) {
      // Improved error parsing
      const errorDetail = error.response?.data?.detail 
        ? error.response.data.detail 
        : typeof error.response?.data?.error === "string"
        ? error.response.data.error
        : "An error occurred while uploading the file.";
      setError(errorDetail);
      setUploading(false);
    } 
  }, [apiurl, setAnalysisResult]);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      handleUpload(acceptedFiles[0]);
    }
  }, [handleUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: "application/pdf",
    multiple: false,
  });

  return (
    <div
      {...getRootProps()}
      className={`upload-card ${isDragActive ? "drag-active" : ""}`}
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
    </div>
  );
};

export default UploadCard;
