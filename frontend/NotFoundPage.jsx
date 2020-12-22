import React from "react";

// THX https://codepen.io/nw/pen/WQmxYY
export class NotFoundPage extends React.Component{
    constructor(props) {
        super(props);
    }

    render(){
        return (<div className="content">

            <canvas className="snow" id="snow"/>
            <div className="main-text">
                <h1>Aw jeez.<br/>That page has gone missing.</h1><a className="home-link" href="/">Hitch a ride back
                home.</a>
            </div>
            <div className="ground">
                <div className="mound">
                    <div className="mound_text">404</div>
                    <div className="mound_spade"/>
                </div>
            </div>
        </div>)
    }

}