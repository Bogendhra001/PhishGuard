import logo from './logo.svg';
import './App.css';
import Input from './Url_input';
import InitialScreen from './initialScreen';
import icon from "./PhishGuard.svg";

function App() {
  return (<div className="App">
      <header className="App-header">
        <img src={icon} className="App-logo" alt="logo" />
        <InitialScreen/>
        <Input/>
      </header>
    </div>
    
  );
}

export default App;
