import React, { Component } from 'react';

import SatelliteIcon from '@material-ui/icons/Satellite';

function fetchPassovers(next, most_recent) {

    var url = '/api/passovers';
    if (next === true) {
        url = url + '?next=true&limit=1';
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

                if (data.data.next_passovers === undefined || data.data.next_passovers.length == 0) {
                    nextPassover = null;
                } else {
                    let newNextDate = data.data.next_passovers[0].timestamp.replace(' ', 'T');
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
            passoverDuration:2*60,
			nextPassover: null,
			untilPassover: null,
            operationIsAdd:false,
            operatorChar:'-',
            color:'#ffe21f'
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
                {operationIsAdd:true, operatorChar:'+', color:"#2ecc40"},
                this.drawCountdownAfterStateChange
            )
        } else if (timeDifferenceWithNext > 0) {
            this.setState(
                {operationIsAdd:false, operatorChar:'-', color:"#ffe21f"},
                this.drawCountdownAfterStateChange,
            )
        } else if (timeDifferenceWithNext <= 0) {
            this.setState(prevState => ({
                mostRecentPassover: prevState.nextPassover,
                nextPassover:null,
                operationIsAdd:true,
                operatorChar:'+',
                color:"#2ecc40"
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
			<span style={{marginLeft: '1.5em', display: 'inherit'}}>
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
