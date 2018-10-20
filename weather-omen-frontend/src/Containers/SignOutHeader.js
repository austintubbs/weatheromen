import React from "react";

function SignOutHeader(props) {
  return (
    <div className="SignOutHeader">
      <nav>
        <div class="nav-wrapper grey darken-3">
          <div className="container">
            <a href="/" class="brand-logo">
              WeatherOmen
            </a>
            <ul id="nav-mobile" class="right hide-on-med-and-down">
              <li>
                <a href="/">Sign Up</a>
              </li>
              <li>
                <a href="/">Login</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default SignOutHeader;
