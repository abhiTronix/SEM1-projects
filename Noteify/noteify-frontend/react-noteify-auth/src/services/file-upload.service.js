import axios from "axios";
import AuthService from "../services/auth.service";
class FileUploadService {
    upload(file, onUploadProgress) {
        const currentUser = AuthService.getCurrentUser();
        var bearer = null;
        if (currentUser) {
            bearer = "Bearer " + currentUser.access_token
            console.log(bearer)
        }
        let formData = new FormData();
        formData.append("file", file);

        return axios.post("http://localhost:8000/posts/uploadfile", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
                Authorization: bearer
            },
            onUploadProgress,
        });
    }

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

export default new FileUploadService();