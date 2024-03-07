/* global chrome */

import { useEffect, useState } from 'react';

function MyComponent() {
  const [url, setUrl] = useState('');
  const [responseData, setResponseData] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const [processing,setProcess]=useState(true);
  const maxRetries = 3; // Maximum number of retries

  useEffect(() => {
    async function fetchData() {
      try {
        // Send message to background script to get URL
        chrome.runtime.sendMessage({ action: 'getURL' }, async (response) => {
          setUrl(response);
          const responses = await fetch(`http://127.0.0.1:8000/classify/${response}`);
          const data = await responses.json();
          setProcess(false);
          console.log(data);
          setResponseData(data);
        });
      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle error
        if (retryCount < maxRetries) {
          // Retry if maximum retries not reached
          setRetryCount(retryCount + 1);
        } else {
          console.error('Maximum retry attempts reached.');
          // Handle maximum retry attempts reached
        }
      }
    }

    fetchData();
  }, [retryCount]); // Retry whenever retryCount changes

  return (
    <div>
      <p>Current URL: {url}</p>
      {processing && (
        <><p>Processing...</p>
        </>
      )}
      {/* Render specific values from responseData */}
      {responseData && (
        <>
          <p>Result: {responseData.result}</p>
          {/* Add more elements to render other data if needed */}
        </>
      )}
    </div>
  );
}

export default MyComponent;
