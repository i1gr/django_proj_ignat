import React, {Component, useState, useEffect} from 'react';
import { useLocation } from 'react-router-dom'
import { useParams } from 'react-router-dom';


//export default function Service(){
//    let data = {}
//
//    let slug = useParams().slug;
//    fetch('/api/service-without-order/' + slug + '/?format=json')
//        .then((response) => response.json())
//        .then((data) => {
//            if (typeof data !== 'undefined' && data !== null){
//                console.log( {
//                    name: data.name,
//                    slug: data.slug,
//                    price: data.price,
//                    text: data.text,
//                });
//                data = {
//                        name: data.name,
//                        slug: data.slug,
//                        price: data.price,
//                        text: data.text,
//                };
//                console.log(data);
//                 }
//                 });
//
//    console.log("state");
//    console.log(data);
//
//    return (
//        <div>
//            <h3>Service Page</h3>
//            <p>name: {data.name}</p>
//            <p>text:  {data.text}</p>
//        </div>
//        )
//}

//
//export default function Service(){
//    const [c, setState] = useState(
//        {
//            name: "unknown",
//            slug: "unknown",
//            price: "unknown",
//            text: "unknown",
//            run_time: "unknown",
//            absolute_url: "unknown",
//        }
//    );
////    let promise = getServiceDetails(setState);
////    console.log('promise: ');
////    console.log(promise);
//
////    const printAddress = () => {
////        promise.then((a) => {
////            return console.log(a);
////        });
////    };
//
//    getServiceDetails(setState);
//    console.log("state");
//    console.log(c);
//
//    return (
//        <div>
//            <h3>Service Page</h3>
//            <p>name: </p>
//            <p>text:  </p>
//        </div>
//        )
//}

export default function Service(){
    const data = getServiceDetails();
    console.log(data)
    return (
        <div>
            <h3>Service Page</h3>
            <p>name: data.name</p>
        </div>
        )
}

function getServiceDetails(){
    const a = new A({})
    const [count, setCount] = React.useState(0);

    let slug = useParams().slug;
    const res = fetch('/api/service-without-order/' + slug + '/?format=json')
        .then((response) => response.json())
        .then((data) => {
            if (typeof data !== 'undefined' && data !== null){
                return {
                    name: data.name,
                    slug: data.slug,
                    price: data.price,
                    text: data.text,
                }; 
            };
    });



    var b;
    res.then((data)=>{
        console.log('res.then');
        console.log(count);
        useEffect((data) => {
            setCount(data);
        }, [])

        console.log(count);

    })
    console.log('a');
    console.log(count);

    return a.data

}


class A{
    data;
    constructor(data) {
        this.data = data;
  }
  speak() {
    console.log(this.data);
  }
}


class ServiceNotWork extends Component {
    constructor(props){
        super(props);
        this.state = {
            name: "unknown",
            slug: "unknown",
            price: "unknown",
            text: "unknown",
            run_time: "unknown",
            absolute_url: "unknown",
        }
        this.getServiceDetails();
    }

    getServiceDetails(){
//        console.log("slug:");
//        console.log(useParams());
        fetch('/api/service-without-order/:slug/?format=json').then((response) =>
            response.json()).then((data) => {
                if (typeof data !== 'undefined' && data !== null){
                    this.setState({
                        test_data: JSON.stringify(data, null, 2),

                        name: data.name,
                        slug: data.slug,
                        price: data.price,
                        text: data.text,
                    });
                };
        });
    }

    render() {
        console.log(useParams());
        return (
        <div>
            <h3>Service Page</h3>
            <p>name: {this.state.name}</p>
            <p>text: {this.state.text}</p>
        </div>
        )
    }
}
