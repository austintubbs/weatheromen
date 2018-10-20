import React, { Component } from "react";
import SignOutHeader from "./SignOutHeader";

class SignIn extends Component {
  state = {
    email: "",
    password: ""
  };
  handleChange = e => {
    this.setState({
      [e.target.id]: e.target.value
    });
  };
  handleSubmit = e => {
    e.preventDefault();
  };
  render() {
    return (
      <div ClassName="SignIn">
        <SignOutHeader />
      </div>
    );
  }
}

export default SignIn;
