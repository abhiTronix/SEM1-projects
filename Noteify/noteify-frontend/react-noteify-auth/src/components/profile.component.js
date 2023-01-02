import React, { Component } from "react";
import { Navigate } from "react-router-dom";
import AuthService from "../services/auth.service";
import UserService from "../services/user.service";
import UploadImages from "./upload-files.component";
import DownloadService from "../services/file-download.service";

export default class Profile extends Component {
  constructor(props) {
    super(props);

    this.state = {
      redirect: null,
      userReady: false,
      currentUser: { username: "" }
    };
    this.download = this.download.bind(this);
  }

  download() {
    DownloadService.downloadFile()
      .then((response) => {
        return response.data
      })
      .catch((err) => {
        console.log(err);
      });
  }

  componentDidMount() {
    const currentUser = AuthService.getCurrentUser();

    UserService.getSubjectcode().then(
      response => {
        this.setState({
          content: Object.values(response.data)
        });
      },
      error => {
        this.setState({
          content:
            (error.response &&
              error.response.data &&
              error.response.data.message) ||
            error.message ||
            error.toString()
        });
      }
    );

    if (!currentUser) this.setState({ redirect: "/login" });
    this.setState({ currentUser: currentUser, userReady: true })
  }

  render() {
    if (this.state.redirect) {
      return <Navigate to={this.state.redirect} />
    }

    const { currentUser } = this.state;

    return (
      <div className="container">
        {(this.state.userReady) ?
          <div>
            <header className="jumbotron">
              <h3>
                <strong>{currentUser.name}</strong> Profile
              </h3>
            </header>
            <p>
              <strong>Token:</strong>{" "}
              {currentUser.access_token.substring(0, 20)} ...{" "}
              {currentUser.access_token.substr(currentUser.access_token.length - 20)}
            </p>
            <p>
              <strong>Username:</strong>{" "}
              {currentUser.username}
            </p>
            <p>
              <strong>Email:</strong>{" "}
              {currentUser.email}
            </p>
            <p>
              <strong>Bearer:</strong>{" "}d
              {currentUser.token_type}
            </p>
            <h4>React Download</h4>
            <button
              onClick={this.download}
            >
              Download
            </button>
            <h4>React Image Upload with Preview</h4>
            <div className="content">
              <UploadImages />
            </div>
          </div> : null
        }

      </div>

    );

  }
}
