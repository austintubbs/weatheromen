import React, { Component } from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import LandingPage from "./Containers/LandingPage";

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          <Switch>
            <Route exact path="/" component={LandingPage} />
          </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
