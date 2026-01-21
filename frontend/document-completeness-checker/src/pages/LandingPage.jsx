import React, { useState, useEffect } from "react";
import UploadCard from "../components/UploadCard";
import Hero from "../components/Hero";
import Navbar from "../components/Navbar";
import ProblemCard from "../components/ProblemCard.jsx";
import axios from "axios";

function LandingPage() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isBackendReachable, setIsBackendReachable] = useState(false);
  const apiurl = import.meta.env.VITE_API_URL || "http://localhost:8000"

  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        const response = await axios.get(`${apiurl}/health`);
            setIsBackendReachable(true);
      } catch (error) {
          setIsBackendReachable(false)
      }
    };

    checkBackendHealth();
  }, []);

  return (
    <>
      <Navbar />
      <Hero />
      {!isBackendReachable && (
        <div className="error">
          The backend is not reachable. Please make sure it is running.
        </div>
      )}
      <UploadCard
        setAnalysisResult={setAnalysisResult}
        isBackendReachable={isBackendReachable}
      />

      {analysisResult && <ProblemCard problems={analysisResult.result} fileName={analysisResult.fileName} />}
    </>
  );
}

export default LandingPage;
