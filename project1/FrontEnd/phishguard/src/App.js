/* global chrome */
// import { useEffect, useState } from 'react';
// // import logo from './logo.svg';
// import './App.css';
// import Input from './Url_input';
// // import InitialScreen from './initialScreen';
// // import icon from "./PhishGuard.svg";
// // import Bard from "./Gemini";
// import MyComponent from './newUrl';
// import phishing from './phishing.png';
// import legit from './legistimate.png';
// import FeatureTable from './featureDisplay';

// function App() {
//   const [url, setUrl] = useState('');
//   const [responseData, setResponseData] = useState(null);
//   const [retryCount, setRetryCount] = useState(0);
//   const [processing,setProcess]=useState(true);
//   const [icon, setIcon]=useState(legit);
//   const maxRetries = 3; // Maximum number of retries

//   useEffect(() => {
//     async function fetchData() {
//       try {
//         // Send message to background script to get URL
//         chrome.runtime.sendMessage({ action: 'getURL' }, async (response) => {
//           setUrl(response);
//           const responses = await fetch(`http://127.0.0.1:8000/classify/${response}`);
//           const data = await responses.json();
//           setProcess(false);
//           if (data.result=="Phishing Website"){
//             setIcon(phishing);
//           }else{
//             setIcon(legit);
//           }
//           console.log(data.features);
//           setResponseData(data);
//         });
//       } catch (error) {
//         console.error('Error fetching data:', error.message);
//         // Handle error
//         if (retryCount < maxRetries) {
//           // Retry if maximum retries not reached
//           setRetryCount(retryCount + 1);
//         } else {
//           console.error('Maximum retry attempts reached.');
//           // Handle maximum retry attempts reached
//         }
//       }
//     }

//     fetchData();
//   }, [retryCount]); 
//   return (<div className="App">
//       <header className="App-header">
//       <div>
//         <img src={icon} className="App-logo" alt="logo" />
//       </div>
//         {/* <InitialScreen/> */}
//         {/* <Bard/> */}
//         <MyComponent url ={ url} responseData={responseData} processing={processing} />
//         <h3>OR</h3>
//         <Input/>
//         <FeatureTable data={responseData.features} processing ={processing}/>
//       </header>
//     </div>
    
//   );
// }

// export default App;
import React from 'react';
import { useEffect, useState } from 'react';
import './App.css';
import Input from './Url_input';
import MyComponent from './newUrl';
import phishing from './phishicon.png';
import legit from './legiticon.png';
import initial from './initial.png';
import FeatureTable from './featureDisplay';

function App() {
  const [url, setUrl] = useState('');
  const [responseData, setResponseData] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const [processing, setProcess] = useState(true);
  const [icon, setIcon] = useState(initial);
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
          if (data.result === "Phishing Website") {
            setIcon(phishing);
          } else {
            setIcon(legit);
          }
          console.log(data.features);
          setResponseData(data);
        });
      } catch (error) {
        console.error('Error fetching data:', error.message);
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
  }, [retryCount]);

  return (
    <div className="App">
      <header className="App-header">
        <div>
          <img src={icon} className="App-logo" alt="logo" />
        </div>
        <MyComponent url={url} responseData={responseData} processing={processing} />
        <h3>OR</h3>
        <Input />
        {responseData && <FeatureTable data={responseData.features} processing={processing} />}
      </header>
    </div>
  );
}

export default App;
