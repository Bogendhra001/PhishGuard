import { useState, useEffect } from 'react';
// import { chrome } from 'webext-polyfill'; // Assuming you're using `webext-polyfill`
import Display from './Display';

function Bard() {
  const [url, setUrl] = useState('');
  const chrome = window.chrome || window.browser;
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    const getActiveTab = async () => {
        try {
            if (chrome && chrome.tabs) {
                const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
                const tab = tabs[0];
                setUrl(tab.url);
            } else {
                setError('chrome.tabs API is not available.');
                // Handle the error (e.g., display an error message)
            }
        } catch (error) {
            setError('Error occurred while fetching active tab:');
            // Handle the error (e.g., display an error message)
        }
    };

    const injectContentScript = () => {
        try {
            if (chrome && chrome.tabs) {
                chrome.tabs.executeScript(null, {
                    file: 'content.js',
                });
            } else {
                setError('chrome.tabs API is not available.');
                // Handle the error (e.g., display an error message)
            }
        } catch (error) {
            setError('Error occurred while injecting content script:');
            // Handle the error (e.g., display an error message)
        }
    };


    getActiveTab();
    injectContentScript();
  }, []);

  const handleSearchTerm = (event) => {
    setSearchTerm(event.target.value);
  };
  return (
    <>
      <div>
        <h1>URL Analysis</h1>
          <>
          {error && <p>Error: {error}</p>}
            <Display data={url} />
          </>
      </div>
    </>
  );
}

  

export default Bard;