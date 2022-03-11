import React, { Component } from 'react';

export default class ProfileDetails extends Component {
    constructor(props){
        super(props);
        this.state = {
            username: "unknown",
            email: "unknown",
            is_staff: false,
        }
        this.getProfileDetails();
    }

    getProfileDetails(){
        fetch('/api/prof/?format=json').then((response) =>
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
            <h1> Hello, {this.state.username}!</h1>
            <h3> It is your profile page. </h3>
            <p>Email: {this.state.email}</p>
            <p>{(() => {
                    if (this.state.is_staff){
                        return "You are staff."
                    }
                    return "You are ordinary user"
                })()
            }</p>
        </div>
        );
    }
}

