import "./Upload.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import axios from "axios";
import Swal from 'sweetalert2';
const Upload = (props) => {
  const [pdfFile, setpdfFile] = useState(null);
  const [pdfFileError, setpdfFileError] = useState("");
  const [viewPdf, setViewPdf] = useState(null);
  const fileType = ["application/pdf", "image/jpg", "image/jpeg", "image/png"];
  const subid = props.subjectidd;
  const handlePdfFileChange = (e) => {
    let selectedFile = e.target.files[0];
    console.log(selectedFile);
    if (selectedFile) {
      console.log(selectedFile.type);
      if (selectedFile && fileType.includes(selectedFile.type)) {
        setpdfFile(selectedFile);
        setpdfFileError("");
        // let reader = new FileReader();
        // reader.readAsDataURL(selectedFile);
        // reader.onloadend = (e) => {
        //   //console.log(e);
        //   setpdfFile(e.target.result);
        //   setpdfFileError("");
        // };
      } else {
        setpdfFile(null);
        setpdfFileError("Please select valid PDF or Image file");
        Swal.fire(
          'Invalid File!',
          'Please select valid PDF or Image file!',
          'error'
        )
      }
    } else {
      console.log("select your file");
    }
  };

  const handlePdfFileSubmit = (e) => {
    e.preventDefault();
    console.log(subid);
    if (pdfFile !== null) {
      let reader = new FileReader();
      reader.readAsDataURL(pdfFile);
      reader.onloadend = (e) => {
        console.log(e.target.result);
        //setpdfFile(e.target.result);
        //setpdfFileError("");
        var user = JSON.parse(localStorage.getItem("user"));
        var bearer = "Bearer " + user.access_token;
        const formdata = new FormData();
        // const headers = {
        //   "Content-Type": pdfFile.type,
        //   Authorization: bearer,
        // };
        // console.log(headers);
        formdata.append("file", pdfFile);
        console.log(formdata);
        axios
          .post("http://172.17.48.124:8000/posts/" + subid, formdata, {
            //.put("http://172.17.48.124:8000/posts/update/" + subid, formdata, {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: bearer,
            },
          })
          .then(function (response) {
            if (response.status !== false) {
              Swal.fire({
                title: 'Upload Success!',
                text: 'File upload successful!',
                icon: 'success',
                timer: 3000,
              }).then(function () {
                window.location.reload();
              });
            }

            console.log(response);
          })
          .catch(function (error) {
            if (error.response) {
              if (error.response.status == 400 || error.response.status == 404 || error.response.status == 500) {
                Swal.fire(
                  'Upload Failure!',
                  'Kindly check your connectivity!',
                  'error'
                )
              }
              // Request made and server responded
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            }
            // else if (error.request) {
            //   // The request was made but no response was received
            //   console.log(error.request);
            // } else {
            //   // Something happened in setting up the request that triggered an Error
            //   console.log('Error', error.message);
            // }

          });
        setViewPdf(e.target.result);
      };
    } else {
      setViewPdf(null);
    }
  };

  if (!props.showUpload) {
    return null;
  } else {
    return (
      <div className="modalUpload" onClick={props.onClose}>
        <div class="inner11" onClick={(e) => e.stopPropagation()}>
          <div class="head11"> File Upload</div>
          <form className="form-group" onSubmit={handlePdfFileSubmit}>
            <div class="bottom">
              <div class="left">
                <div class="text">Upload your Document:</div>
              </div>
              <div class="right">
                {" "}
                <input
                  type="file"
                  className="form-group"
                  required
                  onChange={handlePdfFileChange}
                />
                {pdfFileError ? (
                  <div className="error-msg">{pdfFileError}</div>
                ) : (
                  <div> </div>
                )}
              </div>
            </div>
            <div class="divbottom">
              <button type="submit" className="button-36">
                UPLOAD
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }
};
export default Upload;
