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
            url_api_for_change: '/api/kanban/executor-orders/?format=json&ordering='
        };
        this.getOrders();
    }

    change = () => {
        const url = this.state.url_api_for_change + event.target.value;

        this.setState({
            url_api: url,
            orders: [],
            },
              function () {
                this.getOrders();
            }
        );
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
                url_api: '/api/kanban/all-orders/?format=json&ordering=' + this.state.url_api.split("ordering=")[1],
                url_api_for_change: '/api/kanban/all-orders/?format=json&ordering=',
                orders: [],
                },
                  function () {
                    this.getOrders();
                    console.log(this.state.url_api)
                }
            );
        } else {
            this.setState({
                url_api: '/api/kanban/executor-orders/?format=json&ordering=-data_start',
                url_api_for_change: '/api/kanban/executor-orders/?format=json&ordering=',
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
                <h3>{data.name}</h3>
                <p className="profile">Executor: {this.getNameOrWarning(data.executor)}</p>
                <p className="profile">Customer: {data.customer}</p>
                <p className="date">{data.data_start}</p>
            </div>
        </a>
        );

        const orders_in = this.state.orders.filter((data) => data.kanban_type === 'IN')
        const in_column = orders_in.map((data) =>
        <a href={data.url} className="news-block">
            <div className={"order preview-orders"  + (data.is_user_read ? "" : " unread")}>
                <h3>{data.name}</h3>
                <p className="profile">Executor: {this.getNameOrWarning(data.executor)}</p>
                <p className="profile">Customer: {data.customer}</p>
                <p className="date">{data.data_start}</p>
            </div>
        </a>
        );

        const orders_done = this.state.orders.filter((data) => data.kanban_type === 'DN')
        const done_column = orders_done.map((data) =>
        <a href={data.url} className="news-block">
            <div className={"order preview-orders"  + (data.is_user_read ? "" : " unread")}>
                <h3>{data.name}</h3>
                <p className="profile">Executor: {this.getNameOrWarning(data.executor)}</p>
                <p className="profile">Customer: {data.customer}</p>
                <p className="date">{data.data_start}</p>
            </div>
        </a>
        );

        const orders_ar = this.state.orders.filter((data) => data.kanban_type === 'AR')
        const ar_column = orders_ar.map((data) =>
        <a href={data.url} className="order-block">
            <div className={"preview-orders"  + (data.is_user_read ? "" : " unread")}>
                <h3>{data.name}</h3>
                <p className="profile">Executor: {this.getNameOrWarning(data.executor)}</p>
                <p className="profile">Customer: {data.customer}</p>
                <p className="date">{data.data_start}</p>
            </div>
        </a>
        );

        return(
        <div className="kanban">
            <h1>Kanban Board</h1>

            <h4>
                <input onChange={this.viewAllOrdersHandle} className="checkbox" type="checkbox"/>
                View all orders
            </h4>
            <div>
                    <select onChange={this.change}>
                        <option value="-data_start">start data new</option>
                        <option value="data_start">start data old</option>
                        <option value="-data_end">end data new</option>
                        <option value="data_end">end data old</option>
                        <option value="name">service name</option>
                        <option value="-name">service name - </option>
                        <option value="executor">executor a-z</option>
                        <option value="-executor">executor z-a</option>
                        <option value="customer">customer a-z</option>
                        <option value="-customer">customer z-a</option>
                        <option value="kanban_type">Kanban do-in</option>
                        <option value="-kanban_type">Kanban in-do</option>
                    </select>
            </div>

            <div className="row">
                <div className="column">
                    <h2>Do</h2>

                    <div>{(() => {
                        if (do_column.length >  0){
                            return <div style={{margin: "2.5%"}}>{do_column}</div>
                        }})()}
                    </div>
                </div>

                <div className="column">
                    <h2>In Process</h2>

                    <div>{(() => {
                        if (in_column.length >  0){
                            return <div style={{margin: "2.5%"}}>{in_column}</div>
                        }})()}
                    </div>
                </div>
                <div className="column">
                    <h2>Done</h2>

                    <div>{(() => {
                        if (done_column.length >  0){
                            return <div style={{margin: "2.5%"}}>{done_column}</div>
                        }})()}
                    </div>
                </div>
                <div className="column">
                    <h2>Archive</h2>

                    <div>{(() => {
                        if (ar_column.length >  0){
                            return <div style={{margin: "2.5%"}}>{ar_column}</div>
                        }})()}
                    </div>
                </div>
            </div>



        </div>
        );
    }
}
