import React from "react";

function SignInHeader(props) {
  return (
    <div className="SignInHeader">
      <nav>
        <div class="nav-wrapper grey darken-3">
          <div className="container">
            <a href="/dashboard" class="brand-logo">
              WeatherOmen
            </a>
            <ul id="nav-mobile" class="right hide-on-med-and-down">
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
