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


class LiveCommands extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoaded:false,
            isEmpty:false,
            errorMessage:'',
            textBoxValue:'',
            // TODO replace this with an on-mount fetch to communications
            displayLog:[
                {
                    type:'user-input',
                    data:{message:'ping'}
                },
                {
                    type:'server-response',
                    data:{id:1, message:'Ping response', timestamp:'2019-11-12 01:24:49.005184', sender:'Comm Module', receiver:'Alice'}
                },
                {
                    type:'user-input',
                    data:{message:'ping'}
                },
                {
                    type:'server-response',
                    data:{id:1, message:'Ping response', timestamp:'2019-11-12 01:24:49.005184', sender:'Comm Module', receiver:'Alice'}
                },
                {
                    type:'user-input',
                    data:{message:'ping'}
                },
                {
                    type:'server-response',
                    data:{id:1, message:'Ping response', timestamp:'2019-11-12 01:24:49.005184', sender:'Comm Module', receiver:'Alice'}
                },
                {
                    type:'user-input',
                    data:{message:'ping'}
                },
                {
                    type:'server-response',
                    data:{id:1, message:'Ping response', timestamp:'2019-11-12 01:24:49.005184', sender:'Comm Module', receiver:'Alice'}
                },
                {
                    type:'user-input',
                    data:{message:'ping'}
                },
                {
                    type:'server-response',
                    data:{id:1, message:'Ping response', timestamp:'2019-11-12 01:24:49.005184', sender:'Comm Module', receiver:'Alice'}
                },
            ]
        }

        this.handleOnChange = this.handleOnChange.bind(this);
		this.handleKeyPress = this.handleKeyPress.bind(this);
    }

    handleOnChange(event) {
        this.setState({textBoxValue:event.target.value});
    }

    telecommandIsValid(telecommand) {
        const telecommands = ['ping', 'get-hk', 'turn-on'];
        // TODO: dont use hardcoded list, we should fetch valid telecommands on mount
        if (telecommands.indexOf(telecommand) >= 0) {
            return true;
        }
        return false;
    }

    handleKeyPress(event) {
        // NOTE: we dont prevent default here, TODO understand better
        // event.preventDefault();
        if (event.key === 'Enter') {
            const text = event.target.value
            if (this.telecommandIsValid(text)) {
                console.log(text);
                const logEntry = {type:'user-input', data:{message:text}}
                this.setState(prevState => ({
                  displayLog: [...prevState.displayLog, logEntry], errorMessage:''
                }))
                event.target.value = ''
            } else{
                this.setState({errorMessage:'Invalid Telecommand'})
            }
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
                      onKeyDown={ (event) => this.handleKeyPress(event) }
                      error={!(this.state.errorMessage === '')}
                    />
                </div>
            </div>
        );
    }
}

export default LiveCommands;
