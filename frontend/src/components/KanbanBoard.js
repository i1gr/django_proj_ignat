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


export default class KanbanBoard extends Component {
    constructor(props){
        super(props);
        this.state = {
            orders: Array(),
            url_api: '/api/kanban/executor-orders/?format=json&ordering=-data_start',
        };
        this.getOrders();
    }

    getOrders(){
        fetch(this.state.url_api).then((response) =>
            response.json()).then((data) => {
                for (const new_order of data){
                    this.setState(prevState => ({
                        orders: [...prevState.orders, new_order],
                        })
                    );
                }
        });
    }

    getNameOrWarning(name){
        if (name){
            return name;
        }
        return <em style={{color: "red"}}>None</em>
    }

    viewAllOrdersHandle = () => {
        console.log(event.target.checked)
        if (event.target.checked){
            this.setState({
                url_api: '/api/kanban/all-orders/?format=json&ordering=-data_start',
                orders: [],
                },
                  function () {
                    this.getOrders();
                }
            );
        } else {
            this.setState({
                url_api: '/api/kanban/executor-orders/?format=json&ordering=-data_start',
                orders: [],
                },
                  function () {
                    this.getOrders();
                }
            );
        }
    }

    render(){

        const orders_do = this.state.orders.filter((data) => data.kanban_type === 'DO')
        const do_column = orders_do.map((data) =>
        <a href={data.url} className="news-block">
            <div className={"order preview-orders"  + (data.is_user_read ? "" : " unread")}>
                <h1>{data.name}</h1>
                <p className="date">{data.data_start} - {data.data_end}</p>
                <h6>Executor: {this.getNameOrWarning(data.executor)}, Customer: {data.customer}</h6>
            </div>
        </a>
        );

        const orders_in = this.state.orders.filter((data) => data.kanban_type === 'IN')
        const in_column = orders_in.map((data) =>
        <a href={data.url} className="news-block">
            <div className={"order preview-orders"  + (data.is_user_read ? "" : " unread")}>
                <h1>{data.name}</h1>
                <p className="date">{data.data_start} - {data.data_end}</p>
                <h6>Executor: {this.getNameOrWarning(data.executor)}, Customer: {data.customer}</h6>
            </div>
        </a>
        );

        const orders_done = this.state.orders.filter((data) => data.kanban_type === 'DN')
        const done_column = orders_done.map((data) =>
        <a href={data.url} className="news-block">
            <div className={"order preview-orders"  + (data.is_user_read ? "" : " unread")}>
                <h1>{data.name}</h1>
                <p className="date">{data.data_start} - {data.data_end}</p>
                <h6>Executor: {this.getNameOrWarning(data.executor)}, Customer: {data.customer}</h6>
            </div>
        </a>
        );

        const orders_ar = this.state.orders.filter((data) => data.kanban_type === 'AR')
        const ar_column = orders_ar.map((data) =>
        <a href={data.url} className="news-block">
            <div className={"order preview-orders"  + (data.is_user_read ? "" : " unread")}>
                <h1>{data.name}</h1>
                <p className="date">{data.data_start} - {data.data_end}</p>
                <h6>Executor: {this.getNameOrWarning(data.executor)}, Customer: {data.customer}</h6>
            </div>
        </a>
        );

        return(
        <div style={{color: "red", margin: '1%'}}>
            <h1>Kanban Board</h1>

            <h4>
                <input onChange={this.viewAllOrdersHandle} className="checkbox" type="checkbox"/>
                View all orders
            </h4>

            <div className="row">
                <div className="column" style={{'background-color': "#ccc"}}>
                    <h2>Do</h2>

                    <div>{(() => {
                        if (do_column.length >  0){
                            return <div style={{margin: "5%"}}>{do_column}</div>
                        }})()}
                    </div>
                </div>

                <div className="column" style={{"background-color": "#aaa"}}>
                    <h2>In Process</h2>

                    <div>{(() => {
                        if (in_column.length >  0){
                            return <div style={{margin: "5%"}}>{in_column}</div>
                        }})()}
                    </div>
                </div>
                <div className="column" style={{"background-color": "#ccc"}}>
                    <h2>Done</h2>

                    <div>{(() => {
                        if (done_column.length >  0){
                            return <div style={{margin: "5%"}}>{done_column}</div>
                        }})()}
                    </div>
                </div>
                <div className="column" style={{"background-color": "#aaa"}}>
                    <h2>Archive</h2>

                    <div>{(() => {
                        if (ar_column.length >  0){
                            return <div style={{margin: "5%"}}>{ar_column}</div>
                        }})()}
                    </div>
                </div>
            </div>



        </div>
        );
    }
}
