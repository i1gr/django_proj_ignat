import React, { Component } from "react";
import { render } from "react-dom";
import ProfileNews from "./ProfileNews";
import ProfileDetails from "./ProfileDetails";
import ProfileCustomerOrders from "./ProfileCustomerOrders";
import ProfileExecutorOrders from "./ProfileExecutorOrders";

export default class Orders extends Component {
    render(){
        return(
        <div className='kanban'>
            <ProfileCustomerOrders />
        </div>
        );
    }
}