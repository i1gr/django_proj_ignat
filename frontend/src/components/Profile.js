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
        this.getProfileDetails();
    }

    getProfileDetails(){
        fetch('/prof/?format=json').then((response) =>
            response.json()).then((data) => {
                if (typeof data[0] !== 'undefined' && data[0] !== null){
                    this.setState({
                        test_data: JSON.stringify(data, null, 2),

                        username: data[0].username,
                        email: data[0].email,
                        is_staff: data[0].is_staff,
                    });
                } else {
                    this.setState({
                        test_data: "AnonymousUser",
                        });
                };
        });
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
