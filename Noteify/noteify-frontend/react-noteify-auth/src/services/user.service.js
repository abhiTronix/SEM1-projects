import axios from 'axios';
import authHeader from './auth-header';

const LOGIN_URL = 'http://localhost:8000/';

class UserService {
  getPublicContent() {
    return axios.get(LOGIN_URL); // promise
  }

  getSubjectcode() {
    return axios.get(LOGIN_URL + 'posts/subcodes', { headers: authHeader() });
  }


  /*getUserBoard() {
    const user = JSON.parse(localStorage.getItem('user'));

    return axios.get(USERLOGIN_URL + user.username, { headers: authHeader() });
  }

   
  getAdminBoard() {
    return axios.get(API_URL + 'admin', { headers: authHeader() });
  } */
}

export default new UserService();
