import React, { Component } from "react";
import { render } from "react-dom";
import ProfileNews from "./ProfileNews";
import ProfileDetails from "./ProfileDetails";


export default class Profile extends Component {
    constructor(props){
        super(props);
        this.state = {
            username: "unknown",
            email: "unknown",
            is_staff: false,
            test_data: "have not got a test data",
            articles: Array(),
        };
    }



    render(){
        return(
        <div>
            <ProfileDetails />
            <ProfileNews />
        </div>
        );
    }
}
