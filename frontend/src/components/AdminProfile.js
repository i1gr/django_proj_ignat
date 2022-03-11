import React, { Component } from "react";
import { render } from "react-dom";
import ProfileNews from "./ProfileNews";
import ProfileDetails from "./ProfileDetails";
import ProfileCustomerOrders from "./ProfileCustomerOrders";
import ProfileExecutorOrders from "./ProfileExecutorOrders";


export default class AdminProfile extends Component {
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
            <ProfileExecutorOrders />
            <ProfileCustomerOrders />
            <ProfileNews />
        </div>
        );
    }
}
