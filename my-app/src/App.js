import React, {Component} from "react" 
import Axios from "axios" 
import './Drip.css'
import axios from "axios"

class App extends Component {

  state = {
    seletedFile: null
  }

  fileSelectedHandler = event => {
    this.setState({
      selectedFile: event.target.files[0]
    })
  }

  fileUploadHandler = () => {
    const formData = new FormData();
 
    // Update the formData object
    formData.append(
        'file',
        this.state.selectedFile
    );

    // Details of the uploaded file
    console.log(this.state.selectedFile);

    // Request made to the backend api
    // Send formData object
    axios.post(" http://127.0.0.1:5000/home", formData)
    .then(response => {
      console.log('File uploaded successfully: ', response.data);
    })
    .catch(error => {
        console.error('Error uploading file:', error);
    });
  }


     // File content to be displayed after
    // file upload is complete
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
                      Choose before Pressing the Upload
                      button
                  </h4>
              </div>
          );
      }
  };

  render() {
      return (
          <div className="file-upload-container">
              <h1>Doc Assist</h1>
              <div className="result-section">
              <form className="file-upload-form">
                <label htmlFor="fileInput">Choose a file:</label>
                <input type="file" onChange={this.fileSelectedHandler} />
                <button type="button" onClick={this.fileUploadHandler}>Upload</button>
              </form>
              </div >
              {this.fileData()}
          </div >
      );
  }
}

export default App;