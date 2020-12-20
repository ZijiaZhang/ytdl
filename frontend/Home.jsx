import React from "react";
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
            <h1 style={{textAlign: "center"}}>Youtube Downloader</h1>
            <div className="inputDiv">
                <p>If you have a direct link to the video, you can download it directly.</p>
            <input placeholder="Paste your link here" className="inputSearch" name="q" type="text" onChange={(e) => this.changeDownload(e)}/>
            <Link to={{pathname: "/download", search: "?url="+encodeURIComponent(this.state.download)}}>
                <button className="searchButton">Download</button>
            </Link>
            <br/>
                <p>Or you can search videos on youtube.</p>
                <input placeholder="Enter your keyword here" className="inputSearch" name="q" type="text" onChange={(e) => this.changeSearch(e)}/>
            <Link to={{pathname: "/search", search: "?q="+encodeURIComponent(this.state.queryString)}}>
                <button className="searchButton">Search</button>
            </Link>
            </div>
            </div>
    }
}