/* global chrome */

// import { useEffect, useState } from 'react';
// import phishing from './phishing.png';
// import legit from './legistimate.png';

function MyComponent(props) {
  // const [url, setUrl] = useState('');
  // const [responseData, setResponseData] = useState(null);
  // const [retryCount, setRetryCount] = useState(0);
  // const [processing,setProcess]=useState(true);
  // const [icon, setIcon]=useState(legit);
  // const maxRetries = 3; // Maximum number of retries

  // useEffect(() => {
  //   async function fetchData() {
  //     try {
  //       // Send message to background script to get URL
  //       chrome.runtime.sendMessage({ action: 'getURL' }, async (response) => {
  //         setUrl(response);
  //         const responses = await fetch(`http://127.0.0.1:8000/classify/${response}`);
  //         const data = await responses.json();
  //         setProcess(false);
  //         if (data=="Phishing Website"){
  //           setIcon(phishing);
  //         }else{
  //           setIcon(legit);
  //         }
  //         console.log(data);
  //         setResponseData(data);
  //       });
  //     } catch (error) {
  //       console.error('Error fetching data:', error);
  //       // Handle error
  //       if (retryCount < maxRetries) {
  //         // Retry if maximum retries not reached
  //         setRetryCount(retryCount + 1);
  //       } else {
  //         console.error('Maximum retry attempts reached.');
  //         // Handle maximum retry attempts reached
  //       }
  //     }
  //   }

  //   fetchData();
  // }, [retryCount]); // Retry whenever retryCount changes

  return (
    <>
    <div>
      <p>Current URL: {props.url}</p>
      {props.processing && (
        <><p>Processing...</p>
        </>
      )}
      {/* Render specific values from responseData */}
      {props.responseData && (
        <>
          <p>Result: {props.responseData.result}</p>
          {/* Add more elements to render other data if needed */}
        </>
      )}
    </div>
    </>
  );
}

export default MyComponent;
