import React, { Component } from "react"
import './Drip.css'
import axios from "axios"



class App extends Component {
  
  state = {
    selectedFile: null,
    symptoms: {
      Cough: false,
      Fever: false,
      ShortnessOfBreath: false,
      ChestPain: false,
      Fatigue: false,
      NauseaAndVomiting: false,
      LossOfAppetite: false,
      Confusion: false,
      Headache: false,
      BluishLipsOrNails: false
    },
    pneumoniaChance: null,
    
  }

  fileSelectedHandler = event => {
    this.setState({
      selectedFile: event.target.files[0]
    })
  }

  handleCheckboxChange = event => {
    const { name, checked } = event.target;
    this.setState(prevState => ({
      symptoms: {
        ...prevState.symptoms,
        [name]: checked
      }
    }));
  }

  calculatePneumoniaChance = () => {
    const { symptoms } = this.state;
    const totalWeight = Object.values(symptoms).reduce((acc, checked) => acc + (checked ? 1 : 0), 0);
    const pneumoniaChance = (totalWeight / 26) * 100; // Assuming total weight of symptoms is 26
    this.setState({ pneumoniaChance });
  }

  fileUploadHandler = () => {
    const formData = new FormData();
    formData.append('file', this.state.selectedFile);
    
    axios.post("http://127.0.0.1:5000/home", formData)
      .then(response => {
        console.log('Image percentage: ', response.data);
        this.calculatePneumoniaChance();
      })
      .catch(error => {
        console.error('Error uploading file:', error);
      });
  }


  fileData = () => {
    if (this.state.selectedFile) {
      return (
        <div>
          <h2>File Details:</h2>
          <p>
            File Name:{" "}
            {this.state.selectedFile.name}
          </p>
          <p>
            File Type:{" "}
            {this.state.selectedFile.type}
          </p>
          <p>
            Last Modified:{" "}
            {this.state.selectedFile.lastModifiedDate.toDateString()}
          </p>
        </div>
      );
    } else {
      return (
        <div>
          <br />
          <h4>
            Pneumonia Analysis Description
          </h4>
        </div>
      );
    }
  };

  render() {
    const { symptoms } = this.state;
    return (
      <div className="file-upload-container">
        <h1>Doc Assist</h1>
        <div className="result-section">
          <form className="file-upload-form">
            <div className="checkbox-container" style={{ marginBottom: '40px' }}>
              {Object.entries(symptoms).map(([symptom, checked]) => (
                <label key={symptom}>
                  <input
                    type="checkbox"
                    name={symptom}
                    checked={checked}
                    onChange={this.handleCheckboxChange}
                  /> {symptom}
                </label>
              ))}
            </div>
            <label htmlFor="fileInput">Upload Chest XRay Image:</label>
            <input type="file" onChange={this.fileSelectedHandler} />
            <button type="button" onClick={this.fileUploadHandler} style={{ fontSize: '16px', padding: '10px 20px' }}>Analyze</button>
          </form>
        </div>
        <div style={{ marginBottom: '60px' }}>
          {this.fileData()}
          <div className="text-box">
            <textarea rows="7" cols="50" value={`Percentage Chance of Pneumonia from symptoms: ${this.state.pneumoniaChance || ''}%`} readOnly />
          </div>
        </div>
      </div>
    );
  }
}

export default App;