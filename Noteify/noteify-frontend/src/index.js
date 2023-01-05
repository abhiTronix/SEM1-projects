import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import User from "./User/User";
import Navigation from "./Navigation";
import Sub from "./SubjectPage/Sub.js";
import Upload from "./User/Upload/Upload";
import FileDisp from "./User/FileDisp/FileDisp.js";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <Routes>
      <Route index element={<App />} />
      <Route path="/user" element={<User />} />
      <Route path="/user/file/sub" element={<Sub />} />
      <Route path="/user/file" element={<FileDisp />} />
    </Routes>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
