import React from "react";

function SignOutHeader(props) {
  return (
    <div className="SignOutHeader">
      <nav>
        <div className="nav-wrapper grey darken-3">
          <div className="container">
            <a href="/" className="brand-logo">
              WeatherOmen
            </a>
            <ul className="right hide-on-med-and-down">
              <li>
                <a href="/">Sign Up</a>
              </li>
              <li>
                <a href="/signin">Login</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default SignOutHeader;
