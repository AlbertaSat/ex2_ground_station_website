import React, { Component } from 'react';
import CommunicationsList from './CommunicationsListFull'
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import LinearProgress from '@material-ui/core/LinearProgress';
import Typography from '@material-ui/core/Typography';

// TODO posting messages should refer to current logged in user
// TODO: figue out how to scroll paper automatically as responses are added dynamically

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

function getNewMessages(last_id, ignore) {
    var new_messages = new Promise((resolve, reject) => {
        fetch('/api/communications?last_id=' + last_id + '&ignore_sender=' + ignore)
        .then(results => {
            return results.json();
        }).then(data => {
            if (data.status == 'success') {
                resolve(data.data.messages);
            } else {
                resolve([]);
            }
        });
    });
    return new_messages;
}

class LiveCommands extends Component {
    constructor(props) {
        super(props);
        this.state = {
            splashJobsLeft:2,
            isEmpty:false,
            validTelecommands:[],
            last_id:undefined,
            errorMessage:'',
            textBoxValue:'',
            displayLog:[]
        }
        this.handleChange = this.handleChange.bind(this);
		this.handleKeyPress = this.handleKeyPress.bind(this);
        this.telecommandIsValid = this.telecommandIsValid.bind(this);
        this.updateMessages = this.updateMessages.bind(this);
    }

    componentDidMount() {
        fetch('/api/telecommands',{headers: {'Authorization':'Bearer '+ localStorage.getItem('auth_token')}})
        .then(results => {
            return results.json();
        }).then(data => {
        if (data.status == 'success') {
            this.setState(prevState => ({
                validTelecommands: data.data.telecommands,
                isEmpty: false,
                splashJobsLeft: prevState.splashJobsLeft - 1
            }));
        } else {
            // NOTE: should do something here maybe
            console.log("Error loading telecommands!");
        }
     });
        fetch('/api/communications?max=true',{headers: {'Authorization':'Bearer '+ localStorage.getItem('auth_token')}})
        .then(results => {
            return results.json();
        }).then(data => {
            if (data.status == 'success') {
                const max_message = data.data.messages[0];
                let max_message_id;
                if (max_message !== undefined) {
                    max_message_id = max_message.message_id;
                } else {
                    max_message_id = -1;
                }
                this.setState(prevState => ({
                    last_id: max_message_id,
                    splashJobsLeft: prevState.splashJobsLeft - 1
                }));
            } else {
                // NOTE: should do something here maybe
                console.log('error')
            }
        });
        this.poll_timer = setInterval(
          () => this.updateMessages(),
          1000
        );
    }

    componentWillUnmount() {
        clearInterval(this.poll_timer);
    }

    updateMessages() {
        if (this.state.splashJobsLeft > 0) {
            console.log('splash jobs left!')
            return
        }
        getNewMessages(this.state.last_id, localStorage.getItem('username'))
        .then(new_messages => {
            let last_message = new_messages[new_messages.length - 1];
            if (last_message !== undefined) {
                // let displayable_messages = new_messages.map(message => ({type:'server-message', data:message}))
                this.setState(prevState => ({
                  displayLog: [...prevState.displayLog, ...new_messages],
                  last_id: last_message.message_id
              }));
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
                const post_data = {timestamp:new Date(Date.now()).toISOString(), message:text, sender:localStorage.getItem('username'), receiver:'comm'};

                fetch('/api/communications', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json',
                      'Authorization':'Bearer '+ localStorage.getItem('auth_token')
                    },
                    body: JSON.stringify(post_data),
                }).then(results => {
                    return results.json();
                }).then(data => {
                    if (data.status === 'success') {
                        this.setState(prevState => ({
                          displayLog: [...prevState.displayLog, post_data],
                          errorMessage:'',
                          textBoxValue:''
                      }));
                    } else {
                        // NOTE: should do something here maybe
                        console.log('error')
                    }
                });
            } else{
                this.setState({errorMessage:'Invalid Telecommand'});
            }
        } else if (event.key === 'ArrowUp'){
            // TODO (nice to have): Next level: store input history for easy re-send
            console.log(event.key);
        } else if (event.key === 'ArrowDown') {
            console.log(event.key);
        }
    }

    render() {
        if (this.state.splashJobsLeft > 0) {
            return (
                <div>
                    <LinearProgress />
                </div>
            );
        }
        return (
            <div>
                <div>
                    <Paper style={{height:"70%", overflow: 'auto'}}>
                        <Typography className="header-title" variant="h5" displayInline style={{padding: '10px', margin: '20px'}}>Live Commands</Typography>
                        <CommunicationsList autoScroll={true} displayLog={this.state.displayLog} isEmpty={this.state.isEmpty}/>
                    </Paper>
                </div>
                <div>
                    <TextField
                      id="user-input-textbox"
                      label="Enter Telecommand"
                      margin="normal"
                      variant="outlined"
                      style={{width:"100%","background-color":"white"}}
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
