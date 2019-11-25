import React, { Component } from 'react';

import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import SatelliteIcon from '@material-ui/icons/Satellite';

function fetchPassovers(next, most_recent) {

    var url = '/api/passovers';
    if (next === true) {
        url = url + '?next=true';
    }
    if (most_recent === true) {
        url = url + '&most-recent=true';
    }

    let passovers = new Promise((resolve, reject) => {
        fetch(url)
        .then(results => {
            return results.json();
        }).then(data => {
            if(data.status == 'success'){
                // TODO: check for null
                let nextPassover;
                let mostRecentPassover;

                console.log('RESPONSE', data);
                if (data.data.next_passover === undefined || data.data.next_passover === null) {
                    nextPassover = null;
                } else {
                    let newNextDate = data.data.next_passover.timestamp.replace(' ', 'T');
                    newNextDate.slice(-3);
                    nextPassover = Date.parse(newNextDate);
                }

                if (data.data.most_recent_passover === undefined || data.data.most_recent_passover === null) {
                    mostRecentPassover = null;
                } else {
                    let newMostRecentDate = data.data.most_recent_passover.timestamp.replace(' ', 'T');
                    newMostRecentDate.slice(-3);
                    mostRecentPassover = Date.parse(newMostRecentDate)
                }
                console.log('resolving...' + nextPassover);
                console.log('resolving...' + mostRecentPassover);
                resolve({
                    nextPassover: nextPassover,
                    mostRecentPassover: mostRecentPassover
                });
            }
        })
    });
    return passovers;
}


// inspired by https://www.cssscript.com/minimal-digital-clock-javascript-css/
class Countdown extends Component{
    // passoverDuration is in seconds
	constructor(){
		super();
		this.state = {
			hour: '00',
			minute: '00',
			second: '00',
            displayCountdown:false,
            passoverDuration:5*60,
			nextPassover: null,
			untilPassover: null,
            operationIsAdd:false,
            operatorChar:'-',
            color:'red'
		}

		this.updateCountdown = this.updateCountdown.bind(this);
        this.drawCountdownAfterStateChange = this.drawCountdownAfterStateChange.bind(this);
	}


    componentDidMount() {

        fetchPassovers(true, true).then(data => {
    		this.setState({
                nextPassover: data.nextPassover,
                mostRecentPassover: data.mostRecentPassover,
                displayCountdown: true
            }, this.updateCountdown);
        });

		this.timer = setInterval(
          () => this.updateCountdown(),
          1000
        );
	}


	componentWillUnmount() {
        clearInterval(this.timer);
    }

    drawCountdownAfterStateChange(){
        var utcToday;
		let today =  new Date(Date.now());

		utcToday = new Date(today.getTime() + (today.getTimezoneOffset() * 60000));
        let new_value = this.state.operationIsAdd ? utcToday - this.state.mostRecentPassover : this.state.nextPassover - utcToday;
        console.log(new_value)

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

	updateCountdown(calls_remaining){
        var utcToday;
		let today =  new Date(Date.now());
		utcToday = new Date(today.getTime() + (today.getTimezoneOffset() * 60000));
        var breakout = true;

        // TODO: Check that this.state.nextPassover is not null, same with last passover
        var mostRecentPassover = this.state.mostRecentPassover;
        var nextPassover = this.state.nextPassover;
        if (this.state.mostRecentPassover === null || this.state.nextPassover === null) {
            this.setState({displayCountdown:false});
            clearInterval(this.timer);
            return
        }

        var timeDifferenceWithMostRecent = utcToday - this.state.mostRecentPassover;
        var timeDifferenceWithNext = this.state.nextPassover - utcToday;

        if (timeDifferenceWithMostRecent <= this.state.passoverDuration*1000) {
            this.setState(
                {operationIsAdd:true, operatorChar:'+', color:"green"},
                this.drawCountdownAfterStateChange
            )
        } else if (timeDifferenceWithNext > 0) {
            this.setState(
                {operationIsAdd:false, operatorChar:'-', color:"red"},
                this.drawCountdownAfterStateChange,
            )
        } else if (timeDifferenceWithNext <= 0) {
            this.setState(prevState => ({
                mostRecentPassover: prevState.nextPassover,
                nextPassover:null,
                operationIsAdd:true,
                operatorChar:'+',
                color:"green"
            }), this.drawCountdownAfterStateChange);
            fetchPassovers(true, false).then(data => {
        		this.setState({
                    nextPassover: data.nextPassover
                });
            });
        }
	}


	render(){
        if (!this.state.displayCountdown) {
            return (
                <div></div>
            )
        }
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
