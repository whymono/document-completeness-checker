import React, {useState} from "react";

const UploadCard = () => {

  return (
      <div className="upload-card">
        <h1>Drag & drop your PDF here</h1>
        <input type="file" accept={".pdf"}/>
      </div>
  )
}

export default UploadCard;
