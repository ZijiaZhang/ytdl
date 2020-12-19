import React, {Component} from "react";
import {Link} from "react-router-dom";

export class Home extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            queryString: '',
            download: ''
        }
    }

    changeSearch(event){
        this.setState({'queryString': event.target.value});
    }

    changeDownload(event){
        this.setState({'download': event.target.value});
    }

    render() {
        return <div>
            <input name="q" type="text" onChange={(e) => this.changeDownload(e)}/>
            <Link to={{pathname: "/download", search: "?url="+encodeURIComponent(this.state.download)}}>
                <button>Download</button>
            </Link>

            <input name="q" type="text" onChange={(e) => this.changeSearch(e)}/>
            <Link to={{pathname: "/search", search: "?q="+encodeURIComponent(this.state.queryString)}}>
                <button>Search</button>
            </Link>
            </div>
    }
}