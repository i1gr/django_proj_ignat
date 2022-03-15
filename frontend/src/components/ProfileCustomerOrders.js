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

    render(){
        const orders = this.state.orders.map((data) =>
            <a href={data.url} className="news-block">
                <div className="order preview-orders">
                    <h1>{data.name}</h1>
                    <h3>{data.koban_type_str}</h3>
                    <p className="date">Order date {data.data_start}</p>
                    <p className="date">Estimated order completion date {data.data_end}</p>
                    <p>Executor: {data.executor}</p>
                    <p>{data.text}</p>
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

            <div>{(() => {
                if (this.state.orders.length >  0){
                    return <div style={{margin: "10% 5%"}}>{orders}</div>
                }
                })()}
            </div>
       </div>
        );
    }
}

