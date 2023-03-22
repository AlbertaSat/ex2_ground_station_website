import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

class Logout extends Component{
	componentDidMount() {
		fetch('/api/auth/logout', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + sessionStorage.getItem('auth_token')
			},
			keepalive: true
		});

		sessionStorage.clear('auth_token');
		sessionStorage.clear('username');
		localStorage.clear('auth_token');
		localStorage.clear('username');
  	};

	render(){
		return (<Redirect to='/'/>);
	}
}

export default Logout;