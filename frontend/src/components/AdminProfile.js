import React, { Component } from "react";
import { render } from "react-dom";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import ProfileNews from "./ProfileNews";
import ProfileDetails from "./ProfileDetails";
import ProfileCustomerOrders from "./ProfileCustomerOrders";
import ProfileExecutorOrders from "./ProfileExecutorOrders";


export default class AdminProfile extends Component {
    constructor(props){
        super(props);
        this.state = {
            active: "need-to-do",
        };
    }



    render(){
        const handleClick = () => {
            <ProfileDetails />
        }

        return(
        <div>
            <ProfileDetails />

            <div style={{margin: "5% 0%"}}>
                <a href="/news/add_news" className="button">Create new article</a>
                <a href="/service/add_service/" className="button">Create new service</a>
            </div>

            <div>
                <button onClick={() => this.setState({active: "need-to-do"})} className="button">
                    Need to do
                </button>
                <button onClick={() => this.setState({active: "your-orders"})} className="button">
                    Your orders
                </button>
                <button onClick={() => this.setState({active: "your-articles"})} className="button">
                    Your articles
                </button>
            </div>


            {this.state.active === "need-to-do" && <ProfileExecutorOrders />}
            {this.state.active === "your-orders" && <ProfileCustomerOrders />}
            {this.state.active === "your-articles" && <ProfileNews />}



        </div>
        );
    }
}
