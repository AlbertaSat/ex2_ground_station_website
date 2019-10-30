import React, { Component } from 'react';
import FlightScheduleList from './FlightScheduleList';
import AddFlightschedule from './AddFlightschedule';
import DeleteFlightschedule from './DeleteFlightschedule';

class FlightSchedule extends Component{
	constructor(){
		super();
		this.state = {
			addFlightOpen: false,
			deleteFlightOpen: false,
			allflightschedules: [],
			queuedflightschedule: [],
			thisFlightscheduleCommands: [{'command_id': '', 'time_stamp': ''}],
			thisFlightscheduleId: null,
			availCommands: [{ commandName: 'ping', id: 1 },
  							{ commandName: 'get_hk', id: 2 }]
		}
		this.handleAddFlightOpenClick = this.handleAddFlightOpenClick.bind(this);
		this.handleDeleteFlightOpenClick = this.handleDeleteFlightOpenClick.bind(this);
		this.handleAddEvent = this.handleAddEvent.bind(this);
	};

	handleAddFlightOpenClick(event, idx){
		event.preventDefault();
		event.stopPropagation();

		this.setState({
						addFlightOpen: !this.state.addFlightOpen,
						thisFlightscheduleCommands: [{'command_id': '', 'time_stamp': ''}],
					});
	};

	handleDeleteFlightOpenClick(event){
		event.preventDefault();
		event.stopPropagation();
		this.setState({deleteFlightOpen: !this.state.deleteFlightOpen});
	}

	addFlightschedule(){
		return;
	}

	handleAddEvent(event, type, idx){
		const obj = this.state.thisFlightscheduleCommands.slice();

		if(type=='date'){
			obj[idx].time_stamp = event.toString();
		}else{
			obj[idx].command_id = this.state.availCommands[event.target.dataset.optionIndex].id;
		}
		this.setState({thisFlightscheduleCommands: obj})
		console.log(this.state.thisFlightscheduleCommands);
	}



	render(){
		const flightschedule = [
	      {id: 1, creationDate: '2019-10-10 17:17:52', timeStamp: '2019-10-10 17:17:52', uploadDate: '2019-10-10 17:17:52',
	        commands: [{
	        commandId: 1,
	        commandName: 'ping',
	        timeStamp: '2019-10-10 17:17:52'
	        },
	        {commandId: 2,
	        commandName: 'ddos',
	        timeStamp: '2019-10-10 17:17:52'
	        }
	      ]}];
		return (
		    <div>
    		  <FlightScheduleList 
    		    flightschedule={flightschedule} 
    		    isMinified={false}
    		    handleAddFlightOpenClick={this.handleAddFlightOpenClick}
    		    handleDeleteFlightOpenClick={this.handleDeleteFlightOpenClick}
    		  />
    		  <AddFlightschedule 
    		    open={this.state.addFlightOpen}
    			handleAddFlightOpenClick={this.handleAddFlightOpenClick}
    			handleAddEvent={this.handleAddEvent}
    			thisFlightschedule={this.state.thisFlightscheduleCommands}
    			availCommands={this.state.availCommands}
    		  />
    		  <DeleteFlightschedule
    		    open={this.state.deleteFlightOpen}
    		    handleDeleteFlightOpenClick={this.handleDeleteFlightOpenClick}
    		  />
  			</div>
		)
	}

} 

export default FlightSchedule;