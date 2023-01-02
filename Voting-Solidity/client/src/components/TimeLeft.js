import React, { useState, useEffect, useRef } from "react";
import "../App.css";
import { useNavigate } from "react-router-dom";

const TimeLeft = (props) => {
  const [timerMinutes, setTimerMinutes] = useState("00");
  const [timerSeconds, setTimerSeconds] = useState("00");

  let endtime = new Date(parseInt(props.endtime + "000")).getTime();

  // change directory
  let navigate = useNavigate();

  /* calculate the difference(or the interval) between current time 
  and end time(as per set in the contract) in minutes and seconds  */
  const interval = useRef();

  // Timer function to show the count down.
  const startTimer = () => {
    const countdownDate = endtime;
    let interval = setInterval(() => {
      const now = new Date().getTime();
      const diff = countdownDate - now;

      let minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      let seconds = Math.floor((diff % (1000 * 60)) / 1000);

      if (minutes < 10) {
        minutes = String(minutes).padStart(2, "0");
      }
      if (seconds < 10) {
        seconds = String(seconds).padStart(2, "0");
      }

      if (diff < 0) {
        // stop here
        clearInterval(interval.current);
      } else {
        // update timer
        setTimerMinutes(minutes);
        setTimerSeconds(seconds);
      }
    }, 1000);
  };

  useEffect(() => {
    startTimer();

    return () => {
      clearInterval(interval.current);
    };
  });

  const redirectResults = async () => {
    navigate("/results", { replace: true });
  };

  return (
    <div className="timeZone">
      <button
        type="button"
        className="button-no-btstrp"
        disabled={timerMinutes !== "00"}
        onClick={redirectResults}
      >
        <section className="timer-container">
          <section className="timer">
            <div class="clock">
              {timerMinutes !== "00" ? (
                <>
                  <section>
                    <p>{timerMinutes}</p>
                  </section>
                  <span>:</span>
                  <section>
                    <p>{timerSeconds}</p>
                  </section>
                </>
              ) : (
                <span>Results</span>
              )}
            </div>
          </section>
        </section>
      </button>
    </div>
  );
};

export default TimeLeft;
