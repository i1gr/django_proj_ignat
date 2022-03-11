import React, { Component } from 'react';

export default class ProfileExecutorOrders extends Component {
    constructor(props){
        super(props);
        this.state = {
            orders: Array(),
        },
        this.getOrders();
    }

    getOrders(){
        fetch('/api/executor-orders/?format=json').then((response) =>
            response.json()).then((data) => {
                for (const new_order of data){
                    this.setState(prevState => ({
                        orders: [...prevState.orders, new_order],
                        })
                    );
                }
        });
    }

    render(){
        const orders = this.state.orders.map((data) =>
        <div className="order">
            <h1>{data.name}</h1>
            <h3>{data.koban_type_str}</h3>
            <p className="date">Order date {data.data_start}</p>
            <p className="date">Estimated order completion date {data.data_end}</p>
            <p>Executor: {data.executor}</p>
            <p>{data.text}</p>
        </div>
        );

        return (
            <div>
                <div>{(() => {
                    if (orders.length >  0){
                        return <div style={{margin: "10% 5%"}}><h2>Need to do</h2><hr/>{orders}</div>
                    }
                    })()}
                </div>
            </div>
        );
    }
}


