import React from "react";

function SignInHeader(props) {
  return (
    <div className="SignInHeader">
      <nav>
        <div className="nav-wrapper grey darken-3">
          <div className="container">
            <a href="/dashboard" className="brand-logo">
              WeatherOmen
            </a>
            <ul className="right hide-on-med-and-down">
              <li>
                <a href="/">Logout</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default SignInHeader;
