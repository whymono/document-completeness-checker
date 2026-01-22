import React, { useState, useEffect } from "react";
import UploadCard from "../components/UploadCard";
import Hero from "../components/Hero";
import Navbar from "../components/Navbar";
import ProblemCard from "../components/ProblemCard.jsx";
import axios from "axios";

function LandingPage() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isBackendReachable, setIsBackendReachable] = useState(false);
  const apiurl = import.meta.env.VITE_API_URL

  useEffect(() => {
    const checkBackendHealth = async () => {
      // Log the URL to be sure it's correct
      console.log(`Attempting backend health check at: ${apiurl}/health`);

      // Guard clause: VITE_API_URL might be undefined if .env is not set up.
      if (!apiurl) {
        console.error(
          "CRITICAL: VITE_API_URL is not defined. Please check your .env file."
        );
        setIsBackendReachable(false);
        return;
      }

      try {
        const response = await axios.get(`${apiurl}/health`);

        // Make the success check more robust. Axios only throws for non-2xx
        // statuses by default, but this can be overridden. This check is safer.
        if (response.status >= 200 && response.status < 300) {
          console.log("Backend is reachable. Status:", response.status);
          setIsBackendReachable(true);
        } else {
          // This handles cases where axios is configured NOT to throw on error statuses.
          console.warn(
            `Backend responded with a non-success status: ${response.status}`
          );
          setIsBackendReachable(false);
        }
      } catch (error) {
        // This block will catch network errors or non-2xx responses (if axios is default)
        console.error("Backend is not reachable. Request failed:", error.message);

        // Provide more detailed context from the axios error object
        if (error.response) {
          // The server responded with a status code outside the 2xx range
          console.error(`- Status: ${error.response.status}`);
        } else if (error.request) {
          // The request was made but no response was received
          console.error(
            "- No response received. This could be a CORS issue, a network error, or the server is down."
          );
        }
        setIsBackendReachable(false);
      }
    };

    checkBackendHealth();
  }, [apiurl]);

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
