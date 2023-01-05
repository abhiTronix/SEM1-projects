import "./ImgDisp.css";
import CloseIcon from "@mui/icons-material/Close";
import { useState, useEffect } from "react";

import { display } from "@mui/system";
import AppRej from "./AppRej/AppRej";
import { Document, Page, pdfjs } from "react-pdf";
import Votes from "../Votes/Votes";

import UserButtons from "./Userbuttons";
import Deletebuttons from "./Deletebuttons";

const ImgDisp = (props) => {
  pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;
  const [close, setclose] = useState(false);

  const [detailz, setDetailz] = useState(null);
  var admin = JSON.parse(localStorage.getItem("admin"));
  var user = JSON.parse(localStorage.getItem("user"));
  var bearer = "Bearer " + user.access_token;
  const formatDate = (dateString) => {
    const options = { year: "numeric", month: "long", day: "numeric" };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };
  const [numPages, setNumPages] = useState(null);
  console.log(props.filedetail.Post.subject_code);
  console.log(props.user);

  useEffect(() => {
    fetch(
      "http://172.17.48.124:8000/posts/find/" + props.filedetail.Post.subject_code,
      {
        method: "GET",
        body: JSON.stringify(),
        headers: {
          "Content-Type": "application/json",
          Authorization: bearer,
        },
      }
    ).then((response) => {
      return response.json();
    }).then((data1) => {
      setDetailz(data1);
      console.log(data1);
    });
  }, []);



  const but = () => {
    props.extra(close);
  };

  if (detailz !== null) {
    return (
      <div className="outerbox">
        <div class="close" onClick={but}>
          <CloseIcon color="white" />
        </div>


        <div className="innerbox">

          {/* <img
            src={
              "http://172.17.48.124:8000/data/file/" +
              encodeURIComponent(props.newfile)
            }
          /> */}
          <Document
            file={
              "http://172.17.48.124:8000/data/file/" +
              encodeURIComponent(props.newfile)
            }
            onLoadSuccess={({ numPages }) => setNumPages(numPages)}
          >
            {Array.apply(null, Array(numPages))
              .map((x, i) => i + 1)
              .map((page) => (
                <Page pageNumber={page} />
              ))}
          </Document>
        </div>
        <Votes admin={admin} subjectname={detailz.Post.subject_code} sub_id={detailz.Post.id} />
        <div className="innerbox2">
          <UserButtons admin={admin} filedetail={props.filedetail} newfile={props.newfile} />
          <AppRej admin={admin} filedetail={props.filedetail} />
          <div className={`upu ${admin ? "up" : ""}`}>
            <div class="inner-up">
              <div class="six">
                <div class="up-text">Subject Code</div>
                <div class="up-text1">{detailz.Post.subject_code}</div>
              </div>
              <div class="six">
                <div class="up-text">File Name</div>
                <div class="up-text1">{detailz.Post.curr_version}</div>
              </div>
              <div class="six">
                <div class="up-text">Published</div>
                <div class="up-text1">
                  {detailz.Post.published.toString()}
                </div>
              </div>
            </div>
            <div class="inner-up">
              <div class="six">
                <div class="up-text">Created at</div>
                <div class="up-text1">
                  {formatDate(detailz.Post.created_at)}
                </div>
              </div>
              <div class="six">
                <div class="up-text">File Owner Name</div>
                <div class="up-text1">{detailz.Post.owner_username}</div>
              </div>
              <div class="six">
                <div class="up-text">Votes</div>
                <div class="up-text1">{detailz.votes}</div>
              </div>
            </div>
          </div>
          <Deletebuttons admin={admin} user={props.user} newfile={props.newfile} filedetail={props.filedetail} />
        </div>


      </div>
    );
  }
  else {
    return null;
  }
};
export default ImgDisp;
