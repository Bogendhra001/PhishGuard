/* global chrome */

import { useEffect, useState } from 'react';

function MyComponent() {
  const [url, setUrl] = useState('');
  const [responseData, setResponseData] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        // Send message to background script to get URL
        chrome.runtime.sendMessage({ action: 'getURL' }, async (response) => {
          setUrl(response);
          const responses = await fetch(`http://127.0.0.1:8000/classify/${response}`);
          const data = await responses.json();
          console.log(data);
          setResponseData(data);
        });
      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle error
      }
    }

    fetchData();
  }, []); // Empty dependency array ensures the effect runs only once when the component mounts

  return (
    <div>
      <p>Current URL: {url}</p>
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
