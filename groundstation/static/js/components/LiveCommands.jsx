import React, { Component } from 'react';
import CommunicationsList from './CommunicationsListFull'
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

const useStyles = makeStyles(theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: 200,
  },
}));

// TODO: figue out how to scroll paper automatically as responses are added dynamically

class LiveCommands extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoaded:false,
            isEmpty:false,
            validTelecommands:[],
            errorMessage:'',
            textBoxValue:'',
            // TODO replace this with an on-mount fetch to communications
            displayLog:[
                {
                    type:'user-input',
                    data:{message:'ping'}
                },
                {
                    type:'server-message',
                    data:{id:1, message:'Ping response', timestamp:'2019-11-12 01:24:49.005184', sender:'Comm Module', receiver:'Alice'}
                },
                {
                    type:'user-input',
                    data:{message:'ping'}
                },
                {
                    type:'server-message',
                    data:{id:1, message:'Ping response', timestamp:'2019-11-12 01:24:49.005184', sender:'Comm Module', receiver:'Alice'}
                },
                {
                    type:'user-input',
                    data:{message:'ping'}
                },
                {
                    type:'server-message',
                    data:{id:1, message:'Ping response', timestamp:'2019-11-12 01:24:49.005184', sender:'Comm Module', receiver:'Alice'}
                }
            ]
        }

        this.handleChange = this.handleChange.bind(this);
		this.handleKeyPress = this.handleKeyPress.bind(this);
        this.telecommandIsValid = this.telecommandIsValid.bind(this);
    }

    componentDidMount() {
        fetch('/api/telecommands')
        .then(results => {
            return results.json();
        }).then(data => {
        console.log('data: ', data);
        if (data.status == 'success') {
            this.setState({ validTelecommands: data.data.telecommands, isLoaded: true, isEmpty: false });
        } else {
            // TODO: What should we do here
            console.log("Error loading telecommands!");
        }
     });
    }

    telecommandIsValid(telecommand_string) {
        const split_string = telecommand_string.trim().split(' ');
        const matching_command = this.state.validTelecommands.find((element) => {
            if (element.command_name === split_string[0]) {
                return element
            }
        });
        if (matching_command === undefined) {
            return false;
        }
        if (!(matching_command.num_arguments === split_string.slice(1).length)) {
            return false;
        }
        return true;
    }

    handleChange(event) {
        this.setState({textBoxValue:event.target.value});
    }

    handleKeyPress(event) {
        if (event.key === 'Enter') {
            const text = event.target.value;
            if (this.telecommandIsValid(text)) {
                console.log(text);
                // TODO: maybe add timestamp for when user enterred command
                const logEntry = {type:'user-input', data:{message:text}};
                this.setState(prevState => ({
                  displayLog: [...prevState.displayLog, logEntry],
                  errorMessage:'',
                  textBoxValue:''
                }))
            } else{
                this.setState({errorMessage:'Invalid Telecommand'});
            }
        } else if (event.key === 'ArrowUp'){
            // TODO: Next level: store input history for easy re-send
            console.log(event.key);
        } else if (event.key === 'ArrowDown') {
            console.log(event.key);
        }
    }

    render() {
        return (
            <div>
                <div>
                    <Paper style={{height:"70%", overflow: 'auto'}}>
                        <CommunicationsList displayLog={this.state.displayLog} isEmpty={this.state.isEmpty}/>
                    </Paper>
                </div>
                <div>
                    <TextField
                      id="user-input-textbox"
                      label="Enter Telecommand"
                      margin="normal"
                      variant="outlined"
                      style={{width:"30%","background-color":"white"}}
                      value={this.state.textBoxValue}
                      onChange={(event) => this.handleChange(event)}
                      onKeyDown={(event) => this.handleKeyPress(event) }
                      error={!(this.state.errorMessage === '')}
                    />
                </div>
            </div>
        );
    }
}

export default LiveCommands;
