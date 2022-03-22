import React, { Component } from 'react';

export default class ProfileExecutorOrders extends Component {
    constructor(props){
        super(props);
        this.state = {
            orders: Array(),
            url_api: '/api/executor-orders/?format=json&ordering=-data_start',
        },
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

    change = () => {
        const url = '/api/executor-orders/?format=json&ordering=' + event.target.value;
        this.setState({
            url_api: url,
            orders: [],
            },
              function () {
                this.getOrders();
            }
        );
    }

    render(){
        const orders = this.state.orders.map((data) =>
        <a href={data.url} className="news-block">
            <div className={"order preview-orders"  + (data.is_user_read ? "" : " unread")}>
                <h1>{data.name}</h1>
                <h3>{data.kanban_type_str}</h3>
                <p className="date">Order date {data.data_start}</p>
                <p className="date">Estimated order completion date {data.data_end}</p>
                <p>Executor: {data.executor}</p>
                <p>Customer: {data.customer}</p>
                <p>{data.text}</p>
            </div>
        </a>
        );

        return (
            <div>
                <h2>Need to do</h2><hr/>
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
                        <option value="customer">customer name a-z</option>
                        <option value="-customer">customer name z-a</option>
                    </select>
                </div>

                <div>{(() => {
                    if (orders.length >  0){
                        return <div style={{margin: "10% 5%"}}>{orders}</div>
                    }
                    })()}
                </div>
            </div>
        );
    }
}


