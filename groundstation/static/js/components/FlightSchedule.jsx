import React, { Component } from 'react';
import FlightScheduleList from './FlightScheduleList';
import AddFlightschedule from './AddFlightschedule';
import DeleteFlightschedule from './DeleteFlightschedule';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';
import Paper from '@material-ui/core/Paper';

function isMinified(minify, elemt){
	if(!minify){
	  return elmt
	}else{
	  return
	}
  }

class FlightSchedule extends Component{
	constructor(){
		super();
		this.state = {
			isLoading: true,
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
  			thisFlightScheduleStatus: 2,
  			thisExecutionTime: null,
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
		this.handleExecutionTimeChange = this.handleExecutionTimeChange.bind(this);
	}

	componentDidMount(){
		Promise.all([
	      fetch('/api/flightschedules?limit=5',{headers: {'Authorization':'Bearer '+ localStorage.getItem('auth_token')}}), 
	      fetch('/api/telecommands',{headers: {'Authorization':'Bearer '+ localStorage.getItem('auth_token')}})
	    ]).then(([res1, res2]) => {
	      return Promise.all([res1.json(), res2.json()])
	    }).then(([res1, res2]) => {
	      if(res1.status == 'success'){
			this.setState({'allflightschedules': res1.data.flightschedules, 'isLoading': false});
			if (res1.data.flightschedules.length > 0) {
				this.setState({empty: false})
			}
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
						thisExecutionTime: null,
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
			method: 'DELETE',headers: {'Authorization':'Bearer '+ localStorage.getItem('auth_token')}
		}).then(results => {
			return results.json();
		}).then(data => {
			if(data.status == 'success'){
				const obj = this.state.allflightschedules.slice();
				obj.splice(this.state.thisIndex, 1)
				this.setState({deleteFlightOpen: false,
								thisIndex: null,
								thisFlightscheduleId: null,
								allflightschedules: obj,})
				if (this.state.allflightschedules.length == 0) {
					this.setState({empty: true})
				}

			}
		})
	}

	// add or patch a flightschedule
	addFlightschedule(event){
		event.preventDefault();
		// dependent on what state we are in, the url or method changes
		let data = {status: this.state.thisFlightScheduleStatus, 
					execution_time: this.state.thisExecutionTime,
					commands: this.state.thisFlightscheduleCommands}

		let url = (this.state.editFlight)? 
			'/api/flightschedules/' +  this.state.thisFlightscheduleId : 
			'/api/flightschedules'
		let method = (this.state.editFlight)? 'PATCH' : 'POST'
		this.setState({empty: false})
		console.log('posted data', data);
		fetch(url, {
			method: method,
			headers: {
      		  'Content-Type': 'application/json',
      		  'Authorization':'Bearer '+ localStorage.getItem('auth_token')
      		},
      		body: JSON.stringify(data),	
		}).then(results => {
			return results.json();
		}).then(data => {
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
					thisExecutionTime: null,
				})
			}else{
				if(data.message == 'A Queued flight schedule already exists!'){
					alert('A flight schedule is already queued. Please dequeue it first.');
				}
			}
		});

	}

	// handle any changes in our form fields
	handleAddEvent(event, type, idx){
		const obj = this.state.thisFlightscheduleCommands.slice();
		if(type == 'date'){
			// when the time delta offset is changed, add the number of seconds
			// to the execution time for the command timestamp
			let thisTimeObj = this.state.thisExecutionTime;
			if(this.state.editFlight && !thisTimeObj.endsWith('Z')){
				console.log(this.state.thisExecutionTime)
				thisTimeObj.slice(-3);
				thisTimeObj = thisTimeObj.replace(' ', 'T').concat('Z');
			}
			let thisTime = Date.parse(thisTimeObj);
			let offsetSeconds = parseInt(event.target.value) * 1000;
			thisTime = new Date(thisTime + offsetSeconds);


			obj[idx].timestamp = thisTime.toISOString(); 
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
	}

	handleExecutionTimeChange(event){
		let thisExecutionTime = event._d;
		const obj = this.state.thisFlightscheduleCommands.slice();
		// handle changing all flight schedule command timestamps if the execution 
		// time is changed, that is all flightschedule timestamps should reflect
		// the current execution time plus the offset

		// handle when execution time is null, ie we are creating a new flightschedule
		if(this.state.thisExecutionTime != null){
			let adjustedCommands = obj.map(command => {
				if(command.timestamp){
					// handle a weird bug
					if(command.op == 'add'){
						command.timestamp = command.timestamp.replace('Z', '');
						command.timestamp = command.timestamp.concat('000');
					}
					console.log(command.timestamp, command.op);
					let oldTime = Date.parse(command.timestamp);
					let oldExecTime = Date.parse(this.state.thisExecutionTime);
					let origOffset = oldTime - oldExecTime;
					let newTimestamp = new Date(thisExecutionTime.getTime() + origOffset)

					command.timestamp = newTimestamp.toISOString();
					if(this.state.editFlight){
						if(command.op != 'add' || command.op != 'remove'){
							command.op = 'replace';
						}
					}	
				}
			})
		}
		this.setState({thisExecutionTime: thisExecutionTime.toISOString(), thisFlightscheduleCommands: obj})

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
		let executionTime = this.state.allflightschedules[idx].execution_time;
		const obj = this.state.allflightschedules[idx].commands.map((command) => (
			{...command, op: 'none'}
		))
		console.log(obj);

		this.setState({addFlightOpen: !this.state.addFlightOpen,
						thisFlightscheduleCommands: obj,
						editFlight: true,
						thisFlightscheduleId: id,
						thisIndex: idx,
						thisFlightScheduleStatus: status,
						thisExecutionTime: executionTime,
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
			<Paper className="grid-containers">
			<Grid container style={{paddingBottom: '12px'}}>
				<Grid item xs={11}>
					<Typography variant="h5" displayInline style={{padding: '10px'}}>Flight Schedules</Typography>
				</Grid>
				<Grid item xs={1} style={{textAlign: 'right'}}>
					<Fab style={{position: 'inherit'}}onClick={ (event) => this.handleAddFlightOpenClick(event) }>
						<AddIcon 
								style={{ color: '#4bacb8', fontSize: '2rem'}} 
						/>
					</Fab>
				</Grid>
			</Grid>
			  <FlightScheduleList 
			    isLoading={this.state.isLoading}
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
    			executionTime={this.state.thisExecutionTime}
    			handleQueueClick={this.handleQueueClick}
    			handleExecutionTimeChange={this.handleExecutionTimeChange}
    		  />
    		  <DeleteFlightschedule
    		    open={this.state.deleteFlightOpen}
    		    handleDeleteFlightOpenClick={this.handleDeleteFlightOpenClick}
    		    deleteFlightschedule={this.deleteFlightschedule}
    		    handleDeleteFlightClose={this.handleDeleteFlightClose}
    		  />
			</Paper>
  			</div>
		)
	}

} 

export default FlightSchedule;
