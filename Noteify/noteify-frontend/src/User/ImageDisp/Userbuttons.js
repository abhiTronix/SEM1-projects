import { useEffect, useState } from "react";
import "./ImgDisp.css";
import Qrcode from "../QR/Qrcode"
import Swal from 'sweetalert2';
import axios from "axios";
const UserButtons = (props) => {
    //var user = JSON.parse(localStorage.getItem("user"));
    const [show, setShow] = useState(false);
    function downloadfile() {
        var filename = null;
        let formData = new FormData();
        axios.post('http://localhost:8000/data/download/' + props.filedetail.Post.curr_version, formData, {
            headers: {},
            responseType: 'blob'
        })
            .then(response => {
                console.log(response);
                const disposition = response.headers['content-disposition'];
                filename = disposition.split(/;(.+)/)[1].split(/=(.+)/)[1];
                console.log(filename);
                if (filename.toLowerCase().startsWith("utf-8''"))
                    filename = decodeURIComponent(filename.replace("utf-8''", ''));
                else
                    filename = filename.replace(/['"]/g, '');
                return response.data;
            })
            .then(blob => {
                var url = window.URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a); // append the element to the dom
                a.click();
                a.remove(); // afterwards, remove the element  
            }).catch(function (error) {
                if (error.response) {
                    if (error.response.status == 404) {
                        Swal.fire(
                            'Download Failure!',
                            'File does not exist on server!',
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
    }
    if (!props.admin) {
        return (
            <div>
                <div class="disp3">
                    <button onClick={() => setShow(true)} class="buttonar n">Generate QR code</button>
                    <button onClick={downloadfile} class="buttonar n">Download File</button>
                </div>
                <Qrcode
                    filename={props.newfile}
                    show={show}
                    onClose={() => setShow(false)}
                />
            </div>
        );
    } else {
        return null;
    }
};
export default UserButtons;
