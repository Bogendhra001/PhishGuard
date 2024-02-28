// import display  from "./display";
// export default function Input(){
//     let url="";
//     prt=(e)=>{
//         url=e.target.value;
//     };
//     return(<><div>
//         <form >
//           <label htmlFor='name'>Url:</label><br/>
//           <input type='text' placeholder='Enter a url'/>
//           <button onClick={prt(e)}>Analyse</button>
//         </form>

//     </div>
//     <div>
//         <display url={url}></display>
//     </div></>
//     )   
// }


// import React, { useState } from "react";
// import Display from  './display';

// export default function Input() {
//   const [url, setUrl] = useState("");


//   const handleUrlChange = (e) => {
//     setUrl(e.target.value);
//   };

//   const handleAnalyseClick = (e) => {
//     e.preventDefault(); // Prevent default form submission behavior
//     // You can now use the 'url' state variable as needed
//     setUrl(e.target.value);
//   };

//   return (
//     <>
//       <div>
//         <form>
//           <label htmlFor='name'>Url:</label><br/>
//           {/* Use the 'value' prop to bind the input field to the 'url' state */}
//           <input type='text' placeholder='Enter a url' value={url} onChange={handleUrlChange} />
//           {/* <input type='text' placeholder='Enter a url' value={url}/> */}
//           {/* Pass the event handler function reference, not its result */}
//           <button onClick={handleAnalyseClick}>Analyse</button>
//         </form>
//       </div>
//       <div>
//         {/* Pass the 'url' state as a prop to the Display component */}
//         <Display url={url} />
//       </div>
//     </>
//   );
// }



import React, { useState } from "react";
import Display from './display';

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
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      const data = await response.json();
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
      </div>
      <div>
        {error && <p>Error: {error}</p>}
        {responseData && <Display data={responseData} />}
      </div>
    </>
  );
}
