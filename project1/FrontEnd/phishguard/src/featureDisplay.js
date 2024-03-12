
// import React, { useState } from 'react';

// function FeatureTable(props) {
//     const [count, setCount]=useState(0);
//     let data= props.data[0];
//   // Function to render table rows
//   const updatecount=(v)=>{
//     setCount(count+1)
//   };
//   const renderRows = () => {
//     if (!data || typeof data !== 'object') {
//       // Handle case when props.data is null, undefined, or not an object
//       return (
//         <tr>
//           <td colSpan="2">No data available</td>
//         </tr>
//       );
//     }

//     return Object.keys(data).map((key, index) => (
//         <tr key={index}>
//           <td>{key}</td>
//           <td>{data[key]}</td>
//         </tr>
//       ));
  
//   };
//   return (
//     <div>
//       <h2>Feature Table</h2>
//       {props.processing ? (
//         <p>Loading...</p>
//       ) : (
//         <table>
//           <thead>
//             <tr>
//               <th>Features</th>
//               <th>Values</th>
//             </tr>
//           </thead>
//           <tbody>
//             {renderRows()}
//           </tbody>
//         </table>
//       )}
//     </div>
//   );
// }

// export default FeatureTable;
import React, { useState, useEffect } from 'react';

function FeatureTable(props) {
  const [phishingPercentage, setPhishingPercentage] = useState(0);

  useEffect(() => {
    if (props.data && Array.isArray(props.data) && props.data.length > 0) {
      const dataValues = props.data[0]; // Assuming props.data is an array of objects
      const oneCount = Object.values(dataValues).filter(value => value === 1).length;
      const percentage = (oneCount / 27) * 100;
      setPhishingPercentage(percentage);
    }
  }, [props.data]);

  // Function to render table rows
  const renderRows = () => {
    const data = props.data[0];
    if (!data || typeof data !== 'object') {
      // Handle case when props.data is null, undefined, or not an object
      return (
        <tr>
          <td colSpan="2">No data available</td>
        </tr>
      );
    }

    return Object.keys(data).map((key, index) => (
      <tr key={index}>
        <td>{key}</td>
        <td>{data[key]}</td>
      </tr>
    ));
  };

  return (
    <div>
      <h2>Feature Table</h2>
      <p>Phishing Percentage: {phishingPercentage.toFixed(2)}%</p>
      {props.processing ? (
        <p>Loading...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Features</th>
              <th>Values</th>
            </tr>
          </thead>
          <tbody>
            {renderRows()}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default FeatureTable;
