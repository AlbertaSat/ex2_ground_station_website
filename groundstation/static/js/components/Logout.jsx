import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

class Logout extends Component{
	componentDidMount() {
		localStorage.clear('auth_token');
		localStorage.clear('username');
  	};

	render(){
		return (<Redirect to='/'/>);
	}
}

export default Logout;