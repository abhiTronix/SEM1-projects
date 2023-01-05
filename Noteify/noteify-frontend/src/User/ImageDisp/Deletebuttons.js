import { useEffect, useState } from "react";
import "./ImgDisp.css";
import Swal from 'sweetalert2';
import axios from "axios";
import { useNavigate } from "react-router-dom";


const Deletebuttons = (props) => {
    var user = JSON.parse(localStorage.getItem("user"));
    var bearer = "Bearer " + user.access_token;
    const [pub, setpub] = useState(false);
    console.log(props.user)
    const username = props.user.replace("@", "")
    console.log(username)
    let navigate = useNavigate();
    const deletefile = (address) => {
        Swal.fire({
            title: 'Confirmation!',
            text: 'Do you want to delete this file?',
            icon: 'warning',
            timer: 2000,
        }).then(function () {
            axios.delete(address, {
                //.put("http://172.17.48.124:8000/posts/update/" + subid, formdata, {
                headers: {
                    Authorization: bearer,
                },
            }).then(res => {
                if (res.status !== false) {
                    Swal.fire({
                        title: 'Delete Success!',
                        text: 'Delete file successful',
                        icon: 'info',
                        timer: 2000,
                    }).then(function () {
                        navigate('/user');
                    });
                }
            }).catch(function (error) {
                if (error.response) {
                    if (error.response.status == 500) {
                        Swal.fire(
                            'Publish Error!',
                            'Unable to delete data.',
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
        });

    };
    const deletesub = (address) => {
        Swal.fire({
            title: 'Confirmation!',
            text: 'Do you want to delete all the files in this subject?',
            icon: 'warning',
            timer: 2000,
        }).then(function () {
            axios.delete(address, {}, {
                //.put("http://172.17.48.124:8000/posts/update/" + subid, formdata, {
                headers: {
                    Authorization: bearer,
                },
            }).then(res => {
                if (res.status !== false) {
                    Swal.fire({
                        title: 'Delete Success!',
                        text: 'Delete all files successful',
                        icon: 'info',
                        timer: 2000,
                    }).then(function () {
                        window.location.reload();
                    });
                }
            }).catch(function (error) {
                if (error.response) {
                    if (error.response.status == 500) {
                        Swal.fire(
                            'Publish Error!',
                            'Unable to delete data.',
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
        });

    };
    if (props.admin || username == user.username) {
        if (props.admin) {
            return (
                <div class="down2">
                    {/* <button onClick={() => deletefile("http://172.17.48.124:8000/mhposts/deletefile/" + props.filedetail.Post.owner_username + "/" + props.newfile)} class="buttonar d" role="button">
                        Delete
                    </button> */}
                    <button onClick={() => deletesub("http://172.17.48.124:8000/mhposts/deletesub/" + props.filedetail.Post.subject_code)} class="buttonar da" role="button">
                        Delete All
                    </button>
                </div>
            );
        }
        else {
            return (
                <div class="down2">
                    {/* <button onClick={() => deletefile("http://172.17.48.124:8000/posts/deletefile/" + props.filedetail.Post.subject_code + "/" + props.newfile)} class="buttonar d" role="button">
                        Delete
                    </button> */}
                    <button onClick={() => deletesub("http://172.17.48.124:8000/posts/" + props.filedetail.Post.subject_code)} class="buttonar da" role="button">
                        Delete All
                    </button>
                </div>
            );
        }

    } else {
        return null;
    }
};
export default Deletebuttons;
