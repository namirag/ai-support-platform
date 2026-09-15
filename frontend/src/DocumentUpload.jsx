import { useState } from "react";
import api from "./api";


function DocumentUpload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const uploadDocument = async () => {
    if (!file) {
      setMessage("Please select a PDF or DOCX file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/documents/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setMessage(
        `Uploaded successfully. ${response.data.chunks_added} chunks added.`
      );
      setFile(null);
    } catch (error) {
      setMessage("Unable to upload the document.");
    }
  };

  return (
    <div>
      <h2>Upload Support Document</h2>

      <input
        type="file"
        accept=".pdf,.docx"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadDocument}>Upload</button>

      {message && <p>{message}</p>}
    </div>
  );
}

export default DocumentUpload;