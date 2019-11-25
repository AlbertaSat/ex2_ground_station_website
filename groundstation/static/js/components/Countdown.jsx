import React, { Component } from 'react';

import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import SatelliteIcon from '@material-ui/icons/Satellite';


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
            operationIsAdd:false,
            operatorChar:'-',
            color:'#ab000e'
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

	componentWillUnmount() {
        clearInterval(this.timer);
    }

	updateCountdown(){
		// this seems so ghetto, time sucks
		// but update the time remaining until next passover
		let today =  new Date(Date.now());
		let utcToday = new Date(today.getTime() + (today.getTimezoneOffset() * 60000));

		// if passover is passed clear interval for now
		// TODO probably have different behaviour than just stopping countdown
        let timeDifference = this.state.nextPassover - utcToday;
		if(timeDifference <= 0){
			// clearInterval(this.timer);
			// this.setState({
			// 	hour: '00',
			// 	minute: '00',
			// 	second: '00'
			// })
            this.setState({operationIsAdd:true, operatorChar:'+', color:"#007C40"})

		}

        let new_value = this.state.operationIsAdd ? utcToday - this.state.nextPassover : this.state.nextPassover - utcToday;

		let hour = Math.floor((new_value / (1000 * 60 * 60)) % 24);
		let minute = Math.floor((new_value / (1000 * 60)) % 60);
		let second = Math.floor((new_value / 1000) % 60)

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
			<span style={{marginLeft: '3em', display: 'inherit'}}>
				<span style={{marginRight: '0.5em', color:this.state.color}}>
					<SatelliteIcon style={{fontSize: '1.85em'}}/>
				</span>
				<span style={{color:this.state.color, fontWeight: 'bold', fontSize: '1.25em'}}>
				  T{this.state.operatorChar} {this.state.hour}:{this.state.minute}:{this.state.second}
				 </span>
	        </span>
		)
	}
}

export default Countdown;
