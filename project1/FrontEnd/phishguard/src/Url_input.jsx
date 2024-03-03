


import React, { useState } from "react";
import Display from './Display';

export default function Input() {
  const [url, setUrl] = useState("");
  const [responseData, setResponseData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false); // State for loading indicator

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };

  const handleAnalyseClick = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    setLoading(true); // Set loading to true when request is initiated

    try {
      const response = await fetch(`http://127.0.0.1:8000/classify/${url}`);
      const data = await response.json();
      console.log(data);
      setResponseData(data);
      setError(null);
    } catch (error) {
      setError(error.message);
      setResponseData(null);
    } finally {
      setLoading(false); // Set loading to false when request completes
    }
  };

  return (
    <>
      <div>
        <form>
          <label htmlFor='name'>Url:</label><br/>
          <input type='text' placeholder='Enter a url' value={url} onChange={handleUrlChange} />
          <button onClick={handleAnalyseClick} disabled={loading}>{loading ? 'Loading...' : 'Analyse'}</button> {/* Disable button and show loading text when loading */}
        </form>
        <br></br>
        <div>
        {error && <p>Error: {error}</p>}
        {responseData && <Display data={responseData} />}
      </div>
      </div>
    </>
  );
}
