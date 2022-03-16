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
import AdminProfile from "./AdminProfile";
import Service from "./Service";
import KanbanBoard from "./KanbanBoard";

class App extends Component {
    render(){
        return(
            <div>
            <BrowserRouter>
            <Routes>
                <Route path="/accounts/profile/" element={<Profile/>} />
                <Route path="/accounts/admin-profile/" element={<AdminProfile/>} />
                <Route path="/kanban/" element={<KanbanBoard/>} />
                <Route path="/accounts/service/:slug" element={<Service/>} />
            </Routes>
            </BrowserRouter>
            </div>
        );
    }
}
render(<App/>, document.getElementById('app'))

