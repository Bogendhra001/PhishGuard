import logo from './logo.svg';
import './App.css';
import Input from './Url_input';
// import icon from 'D:\PhishGuard\project1\FrontEnd\phishguard\public\PhishGuard.png';

function App() {
  const prt=()=>{
    console.log("Button clicked");
  }
  return (<div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <Input/>
      </header>
    </div>
    
  );
}

export default App;
