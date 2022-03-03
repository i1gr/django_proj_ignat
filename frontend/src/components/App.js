import React, { Component } from "react";
import { render } from "react-dom";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  Redirect,
} from "react-router-dom";

import Profile from "./Profile";

class App extends Component {
    render(){
        return(
            <div>
            <BrowserRouter>
            <Routes>
                <Route path="/accounts/profile/" element={<Profile/>} />

            </Routes>
            </BrowserRouter>
            </div>
        );
    }
}
render(<App/>, document.getElementById('app'))

