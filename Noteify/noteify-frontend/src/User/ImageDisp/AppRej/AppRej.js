import { useEffect, useState } from "react";
import "./../ImgDisp.css";
import Swal from 'sweetalert2';
import axios from "axios";

const AppRej = (props) => {
  var user = JSON.parse(localStorage.getItem("user"));
  var bearer = "Bearer " + user.access_token;
  const publishh = (status) => {
    axios.put("http://172.17.48.124:8000/mhposts/tpublish/" + props.filedetail.Post.id, {
      published: status
    }, {
      //.put("http://172.17.48.124:8000/posts/update/" + subid, formdata, {
      headers: {
        Authorization: bearer,
      },
    }).then(res => {
      if (res.status !== false) {
        Swal.fire({
          title: 'Publish Success!',
          text: 'Publish status change successful',
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
            'Unable to publish data.',
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
  };
  if (props.admin) {
    return (
      <div>
        <div className="down">
          <button onClick={() => publishh(true)} class="buttonar a" role="button">
            Approve
          </button>
          <button onClick={() => publishh(false)} class="buttonar r" role="button">
            Reject
          </button>
        </div>
      </div>
    );
  } else {
    return null;
  }
};
export default AppRej;
