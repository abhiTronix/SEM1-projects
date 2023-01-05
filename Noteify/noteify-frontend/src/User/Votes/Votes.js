import axios from "axios";
import "./Votes.css";
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import Swal from 'sweetalert2';

const Votes = (props) => {
    var user = JSON.parse(localStorage.getItem("user"));
    var bearer = "Bearer " + user.access_token;

    function handleLike() {
        axios.post("http://172.17.48.124:8000/vote", {
            post_id: props.sub_id,
            dir: 1,
        }, {
            //.put("http://172.17.48.124:8000/posts/update/" + subid, formdata, {
            headers: {
                Authorization: bearer,
            },
        }).then(res => {
            if (res.status !== false) {
                Swal.fire({
                    title: 'Vote Success!',
                    text: 'You voted successfully. Horray :)',
                    icon: 'success',
                    timer: 3000,
                }).then(function () {
                    window.location.reload();
                });
            }
        }).catch(function (error) {
            if (error.response) {
                if (error.response.status == 409) {
                    Swal.fire(
                        'Vote Failure!',
                        'You cannot vote twice!',
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

    function handleDislike() {
        axios.post("http://172.17.48.124:8000/vote", {
            post_id: props.sub_id,
            dir: 0,
        }, {
            //.put("http://172.17.48.124:8000/posts/update/" + subid, formdata, {
            headers: {
                Authorization: bearer,
            },
        }).then(res => {
            if (res.status !== false) {
                Swal.fire({
                    title: 'Downvote Success!',
                    text: 'You downvoted successfully :(',
                    icon: 'info',
                    timer: 3000,
                }).then(function () {
                    window.location.reload();
                });

            }
        }).catch(function (error) {
            if (error.response) {
                if (error.response.status == 409) {
                    Swal.fire(
                        'Vote Failure!',
                        'You cannot downvote twice!',
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
                <div class="divbody">
                    <h4>Click to Vote</h4>
                    <button class="btn" id="green" onClick={handleLike}><ThumbUpIcon fontSize="large" /></button>
                    <button class="btn" id="red" onClick={handleDislike}><ThumbDownIcon fontSize="large" /></button>
                </div>
            </div>
        );
    } else {
        return null;
    }


};
export default Votes;
