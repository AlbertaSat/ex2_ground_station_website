import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import Fab from '@material-ui/core/Fab';
import Select from 'react-select';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';
import AddIcon from '@material-ui/icons/Add';
import AutomatedCommandSequenceList from './AutomatedCommandSequenceList';

class AutomatedCommandSequence extends Component {
    constructor() {
        super();
        this.state = {
            isLoading: true,
            empty: true,
            is_admin: false,
            addCommandOpen: false,
            deleteCommandOpen: false,
            editCommand: false,
            editIndex: null,
            thisCommand: {"command": {"command_id": ""}, "priority": null, "args": []},
            availCommands: [],
            automatedcommands: []
        }

        this.handleAddCommandOpenClick = this.handleAddCommandOpenClick.bind(this);
        this.handleCommandEvent = this.handleCommandEvent.bind(this);
        this.handleChangeArgument = this.handleChangeArgument.bind(this);
        this.addAutomatedCommand = this.addAutomatedCommand.bind(this);
        this.handleEditCommandOpenClick = this.handleEditCommandOpenClick.bind(this);
        this.handleDeleteCommandOpenClick = this.handleDeleteCommandOpenClick.bind(this);
        this.handleRearrangeClick = this.handleRearrangeClick.bind(this);

    }

    componentDidMount() {
        const auth_token = localStorage.getItem('auth_token');
        Promise.all([
            fetch('/api/automatedcommands', {headers: {'Authorization':'Bearer '+ auth_token}}),
            fetch('/api/telecommands', {headers: {'Authorization':'Bearer '+ auth_token}}),
            fetch('/api/users/' + auth_token, {headers: {'Authorization':'Bearer ' + auth_token}})
        ]).then(([res1, res2, res3]) => {
            return Promise.all([res1.json(), res2.json(), res3.json()]);
        }).then(([res1, res2, res3]) => {
            if (res1.status == 'success') {
                this.setState({automatedcommands: res1.data.automatedcommands, isLoading: false});
                if (res1.data.automatedcommands.length > 0) {
                    this.setState({empty: false});
                }
            }
            if (res2.status == 'success') {
                this.setState({availCommands: res2.data.telecommands});
            }
            if (res3.status == 'success') {
                this.setState({is_admin: res3.data.is_admin});
            }
        });
    }

    handleAddCommandOpenClick(event) {
        event.preventDefault();
        event.stopPropagation();

        this.setState({
            addCommandOpen: !this.state.addCommandOpen,
            editCommand: false,
            editIndex: null,
            thisCommand: {"command": {"command_id": ""}, "priority": null, "args": []}
        });

    }

    handleCommandEvent(event) {
        let args = [];
        for (let i = 0; i < event.args; i++) {
            args.push({index: i, argument: ""});
        }
        this.setState(prevState => ({
            thisCommand: {
                ...prevState.thisCommand,
                command: {
                    command_id: event.value,
                    command_name: event.label
                },
                args: args
            }
        }));
    }

    handleChangeArgument(event, arg_idx) {
        const args = this.state.thisCommand.args.slice();
        args[arg_idx].argument = event.target.value;
        this.setState(prevState => ({
            thisCommand: {
                ...prevState.thisCommand,
                args: args
            }
        }));
    }

    addAutomatedCommand(event) {
        event.preventDefault();
        if (this.state.editCommand) {
            this.editAutomatedCommand();
            return;
        }

        let data = this.state.thisCommand;
        data.priority = this.state.automatedcommands.length;
        let url = '/api/automatedcommands';
        this.setState({empty: false});

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("auth_token")
            },
            body: JSON.stringify(data),
        }).then(results => {
            return results.json();
        }).then(data => {
            if (data.status == "success") {
                const obj = this.state.automatedcommands.slice();
                obj.push(data.data);
                this.setState({
                    addCommandOpen: !this.state.addCommandOpen,
                    thisCommand: {"command": {"command_id": ""}, "priority": null, "args": []},
                    automatedcommands: obj
                });
            }
        })
    }

    editAutomatedCommand() {
        // should only be used to edit a command or its arguments, and not the priority
        let data = this.state.thisCommand;
        let id = this.state.thisCommand.automatedcommand_id;

        fetch('/api/automatedcommands/' + id, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("auth_token")
            },
            body: JSON.stringify(data),       
        }).then(results => {
            return results.json();
        }).then(data => {
            if (data.status == "success") {
                const obj = this.state.automatedcommands.slice();
                obj[this.state.editIndex] = data.data;
                this.setState({
                    addCommandOpen: !this.state.addCommandOpen,
                    editCommand: false,
                    editIndex: null,
                    thisCommand: {"command": {"command_id": ""}, "priority": null, "args": []},
                    automatedcommands: obj,
                });
            }
        })
    }

    handleEditCommandOpenClick(event, idx) {
        event.preventDefault();
        event.stopPropagation();

        this.setState({
            addCommandOpen: !this.state.addCommandOpen,
            editCommand: true,
            editIndex: idx,
            thisCommand: this.state.automatedcommands[idx]
        });
    }

    handleDeleteCommandOpenClick(event, idx) {
        event.preventDefault();
        event.stopPropagation();

        this.setState({
            deleteCommandOpen: !this.state.deleteCommandOpen,
            thisCommand: this.state.automatedcommands[idx]
        });
    }

    handleDeleteCommandCloseClick(event) {
        event.preventDefault();

        this.setState({
            deleteCommandOpen: false,
            thisCommand: {"command": {"command_id": ""}, "priority": null, "args": []}
        });
    }

    deleteAutomatedCommand(event) {
        event.preventDefault();
        
        let id = this.state.thisCommand.automatedcommand_id;
        fetch('/api/automatedcommands/' + id,
            {method: 'DELETE', headers: {'Authorization': 'Bearer ' + localStorage.getItem("auth_token")}
        }).then(results => {
            return results.json();
        }).then(data => {
            if (data.status == "success") {
                this.setState({
                    deleteCommandOpen: false,
                    thisCommand: {"command": {"command_id": ""}, "priority": null, "args": []},
                    automatedcommands: data.data.automatedcommands
                });
                if (data.data.length == 0) {
                    this.setState({empty: true});
                }
            }
        });
    }

    handleRearrangeClick(event, idx, up=false) {
        event.preventDefault();
        // handle trying to move the top element up or last element down
        if ((idx == 0 && up == true) || (idx == this.state.automatedcommands.length - 1 && up == false)) {
            return;
        } 
        
        let offset = (up == true) ? -1 : 1;
        let first_url = '/api/automatedcommands/' + this.state.automatedcommands[idx].automatedcommand_id;
        let second_url = '/api/automatedcommands/' + this.state.automatedcommands[idx + offset].automatedcommand_id;

        let first_req = {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("auth_token")
            },
            body: JSON.stringify({priority: idx + offset})
        };
        let second_req = {...first_req, body: JSON.stringify({priority: idx})};

        // two requests are needed here to update the priorities of both commands once rearranged
        Promise.all([
            fetch(first_url, first_req),
            fetch(second_url, second_req)
        ]).then(([res1, res2]) => {
            return Promise.all([res1.json(), res2.json()])
        }).then(([res1, res2]) => {
            if (res1.status == "success" && res2.status == "success") {
                const obj = this.state.automatedcommands.slice();
                obj[idx + offset] = res1.data;
                obj[idx] = res2.data;
                this.setState({automatedcommands: obj});
            }
        });
    }

    render() {
        return (
            <div>
            <Paper className="grid-containers" style={{marginBottom: '20px'}}>
            <Grid container>
                <Grid item xs={11}>
                    <Typography variant="h5" style={{padding: '10px'}}>Automated Command Sequence</Typography>
                </Grid>
				<Grid item xs={1} style={{textAlign: 'right'}}>
                    {this.state.is_admin &&
					<Fab style={{position: 'inherit'}} onClick={ (event) => this.handleAddCommandOpenClick(event) }>
						<AddIcon 
								style={{ color: '#4bacb8', fontSize: '2rem'}} 
						/>
					</Fab>                    
                    }
				</Grid>                
            </Grid>    
            </Paper>

            <Grid container style={{paddingBottom: '12px', justifyContent: 'center'}}>
            <Paper className="grid-containers" style={{minWidth: 650}}>
                <Grid item>
                    <AutomatedCommandSequenceList
                    isLoading={this.state.isLoading}
                    commands={this.state.automatedcommands}
                    handleRearrangeClick={this.handleRearrangeClick}
                    handleEditCommandOpenClick={this.handleEditCommandOpenClick}
                    handleDeleteCommandOpenClick={this.handleDeleteCommandOpenClick}
                    empty={this.state.empty}
                    is_admin={this.state.is_admin}
                    />
                </Grid>
            </Paper>                
            </Grid>
            
            <Dialog open={this.state.addCommandOpen} onClose={(event) => this.handleAddCommandOpenClick(event)}>
                <DialogTitle>Add Commands</DialogTitle>
                <DialogContent style={{textAlign: "center"}}>
                    <DialogContentText style={{textAlign: "left"}}>
                        Choose a command from the drop down below to add to the automated command sequence.
                    </DialogContentText>
                    <Select
                    className="basic-single"
                    classNamePrefix="select"
                    name="color"
                    options={this.state.availCommands.map((command) => (
                        {label: command.command_name, value: command.command_id, args: command.num_arguments}
                    ))}
                    value={
                        {label: this.state.thisCommand.command.command_name,
                        value: this.state.thisCommand.command.command_id }
                    }
                    onChange={(event) => this.handleCommandEvent(event)}
                    isClearable
                    placeholder="Command"/>

                    {this.state.thisCommand.args.map((arg, index) => (
                        <TextField key={index}
                        label={"Argument #" + (index + 1)}
                        margin="normal"
                        variant="outlined"
                        defaultValue={arg.argument}
                        onChange={(event) => this.handleChangeArgument(event, index)} />
                    ))}
                </DialogContent>
                <DialogActions>
                    <Button onClick={(event) => this.handleAddCommandOpenClick(event)} color="primary">Cancel</Button>
                    <Button onClick={(event) => this.addAutomatedCommand(event)} color="primary">Submit</Button>
                </DialogActions>
            </Dialog>

            <Dialog open={this.state.deleteCommandOpen} onClose={(event) => this.handleDeleteCommandCloseClick(event)}>
                <DialogTitle>Are you sure you want to delete this?</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        This will delete this command from the automated command sequence.
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={(event) => this.handleDeleteCommandCloseClick(event)} color="primary">No</Button>
                    <Button onClick={(event) => this.deleteAutomatedCommand(event)} color="primary">Yes</Button>
                </DialogActions>
            </Dialog>
            </div>
        )
    }
}

export default AutomatedCommandSequence;
