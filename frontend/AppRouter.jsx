
import React, {Component} from "react";
import {
    Route,
    Switch
} from "react-router-dom";
import {createBrowserHistory} from 'history';
import {SearchPage} from "./SearchPage";
import {Home} from "./Home";

export const history = createBrowserHistory();

class AppRouter extends Component {

    constructor(props) {
        super(props);

    }


    render() {
        return (
            <Switch>
                <Route exact path="/" component={Home}/>
                <Route path="/search" component={SearchPage}/>
            </Switch>
        );
    }
}

export default AppRouter;