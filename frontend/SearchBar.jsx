import React from "react";
import {Link} from "react-router-dom";

export class SearchBar extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            queryString: props.query || ''
        }
    }
    render() {
        return (<div>
            <input placeholder="Enter your keyword here" className="inputSearch" name="q" type="text" value={this.props.query || ''} onChange={(e) => this.changeSearch(e)}/>
        <Link to={{pathname: "/search", search: "?q="+encodeURIComponent(this.state.queryString)}}>
            <button className="searchButton">Search</button>
        </Link>
        </div>)
    }

    changeSearch(event){
        this.setState({'queryString': event.target.value});
    }
}