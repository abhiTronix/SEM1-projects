import axios from "axios";
import AuthService from "../services/auth.service";

class FileDownloadService {
    // downloadFile() {
    //     const currentUser = AuthService.getCurrentUser();
    //     var bearer = null;
    //     var filename = null;
    //     if (currentUser) {
    //         bearer = "Bearer " + currentUser.access_token
    //         console.log(bearer)
    //     }
    //     fetch('http://localhost:8000/posts/downloadfile', {
    //         method: 'GET',
    //         headers: {
    //             'Authorization': bearer,
    //         }
    //     })
    //         .then(response => {
    //             const disposition = response.headers.get('Content-Disposition');
    //             filename = disposition.split(/;(.+)/)[1].split(/=(.+)/)[1];
    //             if (filename.toLowerCase().startsWith("utf-8''"))
    //                 filename = decodeURIComponent(filename.replace("utf-8''", ''));
    //             else
    //                 filename = filename.replace(/['"]/g, '');
    //             return response.blob();
    //         })
    //         .then(blob => {
    //             var url = window.URL.createObjectURL(blob);
    //             var a = document.createElement('a');
    //             a.href = url;
    //             a.download = filename;
    //             document.body.appendChild(a); // append the element to the dom
    //             a.click();
    //             a.remove(); // afterwards, remove the element
    //         })
    //         .catch(error => {
    //             console.error(error);
    //         });
    // }
    downloadFile() {
        const currentUser = AuthService.getCurrentUser();
        var bearer = null;
        var filename = null;
        if (currentUser) {
            bearer = "Bearer " + currentUser.access_token
            console.log(bearer)
        }
        let formData = new FormData();
        axios.post('http://localhost:8000/posts/downloadfile', formData, {
            headers: {
                Authorization: bearer,
            },
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
            })
            .catch(error => {
                console.error(error);
            });
    }
    // upload(file, onUploadProgress) {
    //     const currentUser = AuthService.getCurrentUser();
    //     var bearer = null;
    //     if (currentUser) {
    //         bearer = "Bearer " + currentUser.access_token
    //         console.log(bearer)
    //     }
    //     let formData = new FormData();
    //     formData.append("file", file);

    //     return axios.post("http://localhost:8000/posts/uploadfile", formData, {
    //         headers: {
    //             "Content-Type": "multipart/form-data",
    //             Authorization: bearer
    //         },
    //         onUploadProgress,
    //     });
    // }

    // getFiles() {
    //     const currentUser = AuthService.getCurrentUser();
    //     var bearer = null;
    //     if (currentUser) {
    //         bearer = "Bearer " + currentUser.access_token
    //         console.log(bearer)
    //     }
    //     return axios.get("http://localhost:8000/posts/subcodes", {
    //         headers: {
    //             "Content-Type": "multipart/form-data",
    //             Authorization: bearer
    //         },
    //     });
    // }
}

export default new FileDownloadService();