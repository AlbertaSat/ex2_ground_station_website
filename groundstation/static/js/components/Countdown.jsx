import React, { Component } from 'react';

import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

// inspired by https://www.cssscript.com/minimal-digital-clock-javascript-css/
class Countdown extends Component{
	constructor(){
		super();
		this.state = {
			hour: '00',
			minute: '00',
			second: '00',
			nextPassover: null,
			untilPassover: null,
		}

		this.updateCountdown = this.updateCountdown.bind(this);
	}

	componentDidMount() {
		fetch('/api/passovers?next-only=true')
		.then(results => {
			return results.json();
		}).then(data => {
			if(data.status == 'success'){
				let date = data.data.passovers[0].timestamp;
				let newDate = date.replace(' ', 'T')
				newDate.slice(-3)
				this.setState({nextPassover: Date.parse(newDate)});
			}
		});
		this.timer = setInterval(
          () => this.updateCountdown(),
          1000
        );
	}

	updateCountdown(){
		// this seems so ghetto, time sucks
		// but update the time remaining until next passover
		let today =  new Date(Date.now());
		let utcToday = new Date(today.getTime() + (today.getTimezoneOffset() * 60000));
		let subtract = this.state.nextPassover - utcToday;

		let hour = Math.floor((subtract / (1000 * 60 * 60)) % 24);
		let minute = Math.floor((subtract / (1000 * 60)) % 60);
		let second = Math.floor((subtract / 1000) % 60)

		hour = (hour < 10)? "0" + hour : hour;
		minute = (minute < 10)? "0" + minute : minute;
		second = (second < 10)? "0" + second: second;

		this.setState({
			hour: hour,
			minute: minute,
			second: second,	
		})

	}


	render(){
		return (
			<div>
			  <Paper className="grid-containers">
			  		<div className="container-text">
			  		  <Table aria-label="simple table">
			  		  	<TableHead>
	                      <TableRow>
	                      	<TableCell align="left" padding="none"><h5>Until Next Passover</h5></TableCell>
	                        <TableCell align="center" padding="none"><h5>{this.state.hour}</h5></TableCell>
	                        <TableCell align="center" padding="none"><h5>:</h5></TableCell>
	                        <TableCell align="center" padding="none"><h5>{this.state.minute}</h5></TableCell>
	                        <TableCell align="center" padding="none"><h5>:</h5></TableCell>
	                        <TableCell align="center" padding="none"><h5>{this.state.second}</h5></TableCell>
	                      </TableRow>
	                    </TableHead>
			  		  </Table>
			  		</div>
			  </Paper>
	        </div>
		)
	}
}

export default Countdown;