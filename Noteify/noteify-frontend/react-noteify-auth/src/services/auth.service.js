import axios from "axios";


const API_URL = "http://localhost:8000/";

class AuthService {
  async login(username, password) {
    const headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
    };
    const form = new FormData();
    form.append('username', username);
    form.append('password', password);
    const response = await axios
      .post(API_URL + "login", form, { timeout: 5000, headers: headers });
    if (response.data.access_token) {
      localStorage.setItem("user", JSON.stringify(response.data));
    }
    return response.data;
  }

  logout() {
    localStorage.removeItem("user");
  }

  register(username, name, email, password) {
    return axios.post(API_URL + "users", {
      username,
      name,
      email,
      password
    });
  }

  getCurrentUser() {
    return JSON.parse(localStorage.getItem('user'));;
  }
}

export default new AuthService();
