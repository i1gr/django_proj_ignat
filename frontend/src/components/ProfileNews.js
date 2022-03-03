import React, { Component } from 'react';

export default class ProfileNews extends Component {
    constructor(props) {
        super(props);
        this.state = {
            articles: Array(),
        };
        this.getProfileNews();
    }

    getProfileNews(){
        fetch('/api/mynews/?format=json').then((response) =>
            response.json())
                .then((data) => {
                    if (typeof data[0] !== 'undefined' && data[0] !== null){
                        for (const new_article of data){
                            this.setState(prevState => ({
                                articles: [...prevState.articles, new_article],
                            }));
                        }
                    }
                });
     }

    render(){
        const articles = this.state.articles.map((data) => <a className="news-block" href={data.absolute_url}>
            <div className="preview">
                <h1>{data.title}</h1>
                <p className="date">{data.datetime}</p>
                <p className="article">{data.text}</p>
                <p>Stars: {data.stars}</p>
            </div>
        </a>)

        return(
            <div>{(() => {
                if (this.state.articles.length >  0){
                    return <div style={{margin: "10% 5%"}}><h2>Your Articles</h2><hr/>{articles}</div>
                }
                })()}
            </div>
        );
    }
}

