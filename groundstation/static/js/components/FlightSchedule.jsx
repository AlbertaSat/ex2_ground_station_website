import React, { Component } from 'react';
import FlightScheduleList from './FlightScheduleList';
import AddFlightschedule from './AddFlightschedule';
import DeleteFlightschedule from './DeleteFlightschedule';

class FlightSchedule extends Component{
	constructor(){
		super();
		this.state = {
			empty: true,
			addFlightOpen: false,
			deleteFlightOpen: false,
			editFlight: false,
			allflightschedules: [],
			thisFlightscheduleCommands: [{'command': {'command_id': ''}, 'timestamp': null, 'args' : []}],
			thisFlightscheduleId: null,
			thisIndex: null,
			availCommands: [],
  			patchCommands: [],
  			thisFlightScheduleStatus: 2
		}
		this.handleAddFlightOpenClick = this.handleAddFlightOpenClick.bind(this);
		this.handleDeleteFlightOpenClick = this.handleDeleteFlightOpenClick.bind(this);
		this.handleAddEvent = this.handleAddEvent.bind(this);
		this.addFlightschedule = this.addFlightschedule.bind(this);
		this.handleAddCommandClick = this.handleAddCommandClick.bind(this);
		this.handleEditCommandClick = this.handleEditCommandClick.bind(this);
		this.deleteFlightschedule = this.deleteFlightschedule.bind(this);
		this.handleDeleteFlightClose = this.handleDeleteFlightClose.bind(this);
		this.handleDeleteCommandClick = this.handleDeleteCommandClick.bind(this);
		this.handleChangeArgument = this.handleChangeArgument.bind(this);
		this.handleQueueClick = this.handleQueueClick.bind(this);
	}

	componentDidMount(){
		Promise.all([
	      fetch('/api/flightschedules?limit=5'), 
	      fetch('/api/telecommands')
	    ]).then(([res1, res2]) => {
	      return Promise.all([res1.json(), res2.json()])
	    }).then(([res1, res2]) => {
	      if(res1.status == 'success'){
	        this.setState({'allflightschedules': res1.data.flightschedules, empty: false});
	      }if(res2.status == 'success'){
	        this.setState({availCommands: res2.data.telecommands})
	      }
	    });
	}

	// handle add flight screen open
	handleAddFlightOpenClick(event){
		event.preventDefault();
		event.stopPropagation();

		this.setState({
						addFlightOpen: !this.state.addFlightOpen,
						editFlight: false,
						thisFlightscheduleId: null,
						thisIndex: null,
						thisFlightscheduleCommands: [{'command': {'command_id': ''}, 'timestamp': null, 'args': []}],
						thisFlightScheduleStatus: 2,
					});
	};

	// handle opening of delete flight schedule dialog
	handleDeleteFlightOpenClick(event, idx, id){
		event.preventDefault();
		event.stopPropagation();
		this.setState({deleteFlightOpen: !this.state.deleteFlightOpen,
						thisFlightscheduleId: id,
						thisIndex: idx});
	}

	//handle closing of delete flight schedule dialog
	handleDeleteFlightClose(event){
		event.preventDefault();
		this.setState({deleteFlightOpen: false,
						thisFlightscheduleId: null,
						thisIndex: null});
	}

	// handle deletion of flight schedule
	deleteFlightschedule(event){
		event.preventDefault();
		fetch('/api/flightschedules/' + this.state.thisFlightscheduleId, {
			method: 'DELETE',
		}).then(results => {
			return results.json();
		}).then(data => {
			console.log(data);
			if(data.status == 'success'){
				console.log(this.state.thisIndex);
				const obj = this.state.allflightschedules.slice();
				obj.splice(this.state.thisIndex, 1)
				console.log(obj)
				this.setState({deleteFlightOpen: false,
								thisIndex: null,
								thisFlightscheduleId: null,
								allflightschedules: obj})

			}
		})
	}

	// add or patch a flightschedule
	addFlightschedule(event){
		event.preventDefault();
		// dependent on what state we are in, the url or method changes
		let data = {status: this.state.thisFlightScheduleStatus, commands: this.state.thisFlightscheduleCommands}
		let url = (this.state.editFlight)? 
			'/api/flightschedules/' +  this.state.thisFlightscheduleId : 
			'/api/flightschedules'
		let method = (this.state.editFlight)? 'PATCH' : 'POST'
		console.log('posted data', data);
		fetch(url, {
			method: method,
			headers: {
      		  'Content-Type': 'application/json'
      		},
      		body: JSON.stringify(data),	
		}).then(results => {
			return results.json();
		}).then(data => {
			console.log(data)

			if(data.status == 'success'){
				const obj = this.state.allflightschedules.slice();
				// depending on what we are doing, we handle the resulting data differently
				if(this.state.editFlight){
					obj[this.state.thisIndex] = data.data;
				}else{
					obj.push(data.data);
				}
				this.setState({addFlightOpen: !this.state.addFlightOpen,
					thisFlightscheduleCommands: 
						[{'command': {'command_id': ''}, 'timestamp': '', 'args': []}],
					allflightschedules: obj,
					editFlight: false,
					thisIndex: null,
					thisFlightscheduleId: null,
					thisFlightScheduleStatus: 2,
				})
			}
		});

	}

	// handle any changes in our form fields
	handleAddEvent(event, type, idx){
		console.log('event', event)
		const obj = this.state.thisFlightscheduleCommands.slice();
		if(type=='date'){
			obj[idx].timestamp = event.toISOString(); 
		}else{
			obj[idx].command.command_id = event.value;
			obj[idx].command.command_name = event.label;
			obj[idx].args = []
			for(let i = 0; i < event.args; i++){
				obj[idx].args.push({index: i, argument: ''})
			}
		}
		// if a command was created and then edited, we consider it added
		// and not replaced, only existing commands can be replaced
		if(this.state.editFlight && obj[idx].op != 'add'){
			obj[idx].op = 'replace'
		}
		// we have to handle the case where an object is being edited,
		// however it is newly created, so deleting it shouldnt be
		// patched to the database
		this.setState({thisFlightscheduleCommands: obj})
		console.log(this.state.thisFlightscheduleCommands);
	}

	// handle changing/adding arguments
	handleChangeArgument(event, fs_idx, arg_idx){
		const obj = this.state.thisFlightscheduleCommands.slice();
		obj[fs_idx].args[arg_idx].argument = event.target.value;
		if(this.state.editFlight && obj[fs_idx].op != 'add'){
			obj[fs_idx].op = 'replace'
		}

		this.setState({thisFlightscheduleCommands: obj})
	}

	// handle when the add command button is clicked
	handleAddCommandClick(event){
		const obj = this.state.thisFlightscheduleCommands.slice();
		let comm = {'command' : {'command_id': ''}, 'timestamp': null, 'args': []}
		// if we are editing add a condition for adding
		if(this.state.editFlight){
			comm.op = 'add'
		}
		obj.push(comm)
		this.setState({thisFlightscheduleCommands: obj})
	}

	// handle deleting a command
	handleDeleteCommandClick(event, idx){
		const obj = this.state.thisFlightscheduleCommands.slice();
		// if a flight schedule is newly created we just want to remove it
		if(obj[idx].op == 'none' || obj[idx].op == 'replace'){
			obj[idx].op = 'remove'
		}else{
			obj.splice(idx, 1)
			console.log('obj', obj)
		}
		this.setState({thisFlightscheduleCommands: obj})
		console.log(this.state.thisFlightscheduleCommands);
	}

	// handle opening the editing dialog
	handleEditCommandClick(event, idx, id){
		event.preventDefault();
		event.stopPropagation();
		// if the flightschedule is queued, we set the state
		// so the button can show the correct value
		let status = this.state.allflightschedules[idx].status;
		const obj = this.state.allflightschedules[idx].commands.map((command) => (
			{...command, op: 'none'}
		))
		this.setState({addFlightOpen: !this.state.addFlightOpen,
						thisFlightscheduleCommands: obj,
						editFlight: true,
						thisFlightscheduleId: id,
						thisIndex: idx,
						thisFlightScheduleStatus: status
						});
	}

	// handles if we have queued a schedule or not based on the current state of is_queued
	handleQueueClick(event){
		event.preventDefault();
		let thisIsQueued = ((this.state.thisFlightScheduleStatus == 1)? 2 : 1);
		this.setState({thisFlightScheduleStatus: thisIsQueued});
	}


	render(){
		return (
		    <div>
    		  <FlightScheduleList 
    		    flightschedule={this.state.allflightschedules} 
    		    isMinified={false}
    		    handleAddFlightOpenClick={this.handleAddFlightOpenClick}
    		    handleDeleteFlightOpenClick={this.handleDeleteFlightOpenClick}
    		    handleEditCommandClick={this.handleEditCommandClick}
    		    empty={this.state.empty}
    		  />
    		  <AddFlightschedule 
    		    open={this.state.addFlightOpen}
    			handleAddFlightOpenClick={this.handleAddFlightOpenClick}
    			handleAddEvent={this.handleAddEvent}
    			thisFlightschedule={this.state.thisFlightscheduleCommands}
    			availCommands={this.state.availCommands}
    			addFlightschedule={this.addFlightschedule}
    			handleAddCommandClick={this.handleAddCommandClick}
    			handleDeleteCommandClick={this.handleDeleteCommandClick}
    			handleChangeArgument={this.handleChangeArgument}
    			status={this.state.thisFlightScheduleStatus}
    			handleQueueClick={this.handleQueueClick}
    		  />
    		  <DeleteFlightschedule
    		    open={this.state.deleteFlightOpen}
    		    handleDeleteFlightOpenClick={this.handleDeleteFlightOpenClick}
    		    deleteFlightschedule={this.deleteFlightschedule}
    		    handleDeleteFlightClose={this.handleDeleteFlightClose}
    		  />
  			</div>
		)
	}

} 

export default FlightSchedule;
