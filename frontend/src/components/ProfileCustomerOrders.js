import React, { Component } from 'react';

export default class ProfileCustomerOrders extends Component {
    constructor(props){
        super(props);
        this.state = {
            orders: Array(),
            url_api: '/api/customer-orders/?format=json',
        },
        this.getOrders();
    }

    change = () => {
        const url = '/api/customer-orders/?format=json&ordering=' + event.target.value;

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
        return <em style={{color: "red"}}>Wait for a executor</em>
    }

    render(){
        const orders_do = this.state.orders.filter((data) => data.kanban_type === 'DO')
        const do_column = orders_do.map((data) =>
        <a href={data.url} className="news-block">
            <div className={"order preview-orders"  + (data.is_user_read ? "" : " unread")}>
                <h3>{data.name}</h3>
                <p className="profile">Executor: {this.getNameOrWarning(data.executor)}</p>
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
                <p className="date">{data.data_start}</p>
            </div>
        </a>
        );

        const orders_ar = this.state.orders.filter((data) => data.kanban_type === 'AR')
        const ar_column = orders_ar.map((data) =>
        <a href={data.url} className="news-block">
            <div className={"order preview-orders"  + (data.is_user_read ? "" : " unread")}>
                <h3>{data.name}</h3>
                <p className="profile">Executor: {this.getNameOrWarning(data.executor)}</p>
                <p className="date">{data.data_start}</p>
            </div>
        </a>
        );


        return(
        <div>
            <h2>Your Orders</h2><hr/>

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
                            return <div style={{margin: "2.5%"}}></div>
                        }})()}
                    </div>
                </div>
            </div>


       </div>
        );
    }
}

