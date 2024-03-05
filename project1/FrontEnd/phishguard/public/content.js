chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message === 'getSearchTerm') {
      const searchBarValue = document.querySelector('input[type="search"]').value; // Modify selector as needed
      sendResponse(searchBarValue);
    }
  });