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
			allflightschedules: null,
			queuedflightschedule: null,
		}
		this.handleAddFlightOpenClick = this.handleAddFlightOpenClick.bind(this);
		this.handleDeleteFlightOpenClick = this.handleDeleteFlightOpenClick.bind(this);
	};

	handleAddFlightOpenClick(event){
		event.preventDefault();
		event.stopPropagation();
		this.setState({addFlightOpen: !this.state.addFlightOpen});
	};

	handleDeleteFlightOpenClick(event){
		event.preventDefault();
		event.stopPropagation();
		this.setState({deleteFlightOpen: !this.state.deleteFlightOpen});
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