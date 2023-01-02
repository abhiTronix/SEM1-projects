import axios from "axios";
import AuthService from "../services/auth.service";

const currentUser = AuthService.getCurrentUser();
var bearer = null;
if (currentUser) {
    bearer = "Bearer " + currentUser.access_token
    console.log(bearer)
}

export default axios.create({
    baseURL: "http://localhost:8000/posts",
    headers: {
        "Content-type": "application/json",
        Authorization: bearer
    }
});