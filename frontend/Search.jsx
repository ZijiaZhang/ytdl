import React, {Component} from "react";

export class Search extends React.Component{
    constructor(props) {
        super(props);
        this.state = {results: []}
        this.params = new URLSearchParams(window.location.search)
    }

    render() {
        return this.state.results.map((data)=> <SearchResult thumbnails={data.thumbnails} url_suffix={data.url_suffix} title={data.title} key={data.title}/>)
    }

    componentDidMount() {
        fetch('/api/search?q='+ encodeURIComponent(this.params.get('q')))
            .then((response) => response.json())
            .then((data) => this.setState({results: data}))
    }

}

class SearchResult extends React.Component{

    constructor(props) {
        super(props);
    }


    render() {
        let url = `url(/proxy?${this.props.thumbnails})`
        console.log(url)
        return(
          <div className="wrapper">
              <div className="inner-wrapper">
                  <div className="card" style={{backgroundImage: url}}>
                      <div className="card__content">
                          <a className="play-button" href={`https://www.youtube.com${this.props.url_suffix}`}>
                              <svg version="1.1" viewBox="0 0 50 50" x="0px"
                                   xmlns="http://www.w3.org/2000/svg"
                                   y="0px">
                                  <path className="polygon" d="M42.7,42.7L25,50L7.3,42.7L0,25L7.3,7.3L25,0l17.7,7.3L50,25L42.7,42.7z"/>
                                  <polygon points="32.5,25 21.5,31.4 21.5,18.6 "/>
                              </svg>
                          </a>

                      </div>

                  </div>
                  <div className="card__content--description">
                      <a>{this.props.title}</a>
                      <form action="/proxy-download" method="get">
                          <input name="url" style={{display: "none"}}
                                 value={`https://www.youtube.com${this.props.url_suffix}`} readOnly/>
                          <button type="submit">Proxy Download</button>
                      </form>
                      <form action="/direct-download" method="get">
                          <input name="url" style={{display: "none"}}
                                 value={`https://www.youtube.com${this.props.url_suffix}`} readOnly/>
                          <button type="submit">Direct Download</button>
                      </form>
                  </div>
              </div>
          </div>)
      }
}

