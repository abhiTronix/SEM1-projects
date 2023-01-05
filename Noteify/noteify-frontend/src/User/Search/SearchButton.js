import "../../SubjectPage/sub.css";

const SearchButton = (props) => {
  if (props.admin) {
    return null;
  } else {
    return (
      <div>
        <button
          onClick={() => props.setShowUpload(true)}
          class="button-9"
          role="button"
        >
          Upload Your File
        </button>
      </div>
    );
  }
};
export default SearchButton;
