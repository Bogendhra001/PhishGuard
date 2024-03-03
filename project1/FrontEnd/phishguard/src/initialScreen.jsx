/* global chrome */


import React, { useState, useEffect } from "react";
import Display from './Display';

const InitialScreen = () => {
  const [responseData, setResponseData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false); // State for loading indicator

  useEffect(() => {
    // Function to fetch URL from active tab
    const fetchUrlFromActiveTab = async () => {
      setLoading(true); // Set loading to true when request is initiated
      try {
        // Get active tab details
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        // Send message to content script to get URL from active tab
        chrome.tabs.sendMessage(tab.id, { type: 'GET_URL' }, async (response) => {
          if (response && response.url) {
            const url = response.url;
            console.log(url);
            const fetchedResponse = await fetch(`http://127.0.0.1:8000/classify/${url}`);
            const data = await fetchedResponse.json();
            setResponseData(data);
            setError(null);
          } else {
            setError("Unable to fetch URL from the active tab.");
            setResponseData(null);
          }
          setLoading(false); // Set loading to false when request completes
        });
      } catch (error) {
        setError(error.message);
        setResponseData(null);
        setLoading(false); // Set loading to false when request completes
      }
    };

    fetchUrlFromActiveTab(); // Fetch URL from active tab when component mounts
  }, []); // Empty dependency array to run effect only once on mount

  return (
    <>
      <div>
        <h1>URL Analysis</h1>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <>
            {error && <p>Error: {error}</p>}
            {responseData && <Display data={responseData} />}
          </>
        )}
      </div>
    </>
  );
}


export default InitialScreen;