import React from "react";

const ProblemCard = ({ problems }) => {
  return (
    <div className="problem-card">
      <h2>Analysis Results</h2>
      {problems && problems.length > 0 ? (
        <div className="problems-list">
          {problems.map((problem, index) => (
              (problem.confidence < 0.8) && <div key={index} className="problem-item">
                <h3>{problem.issue}</h3>
                <p><strong>Confidence:</strong> {problem.confidence}</p>
                </div>
              ))}
        </div>
      ) : (
        <p>No problems found.</p>
      )}
    </div>
  );
};

export default ProblemCard;
