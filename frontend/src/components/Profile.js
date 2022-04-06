import React, { Component } from "react";
import { render } from "react-dom";
import ProfileNews from "./ProfileNews";
import ProfileDetails from "./ProfileDetails";
import ProfileCustomerOrders from "./ProfileCustomerOrders";
import ProfileExecutorOrders from "./ProfileExecutorOrders";


export default class Profile extends Component {
    render(){
        return(
        <div>
            <ProfileDetails />
        </div>
        );
    }
}
