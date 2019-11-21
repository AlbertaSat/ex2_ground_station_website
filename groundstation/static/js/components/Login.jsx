import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import Grid from '@material-ui/core/Grid';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';

const styles = {
  root: {
    padding: '42px',
    display: 'inline-flex',
    alignItems: 'center'
  },
};


class Login extends Component {
    constructor(){
        super();
        this.state = {
            username : null,
            password : null,
            auth_token : null,
            redirect : false,
            error_message : ''
        }
        this.handleUserChange = this.handleUserChange.bind(this);
        this.handlePassChange = this.handlePassChange.bind(this);
        this.handleLogin = this.handleLogin.bind(this);
    };

    handleUserChange(event){
        this.setState({username: event.target.value});
    };

    handlePassChange(event){
        this.setState({password: event.target.value});
    };

    handleLogin(){
        // console.log("user: "+this.state.username+" password: "+this.state.password);

        event.preventDefault();
        let data = {username:this.state.username, password:this.state.password};
        
        // console.log(data)
        let method = 'POST';
        let options = { method: method, 
                        headers: {
                            'Content-Type': 'application/json'
                        }, 
                        body: JSON.stringify(data)};
        fetch('/api/auth/login', options)
            .then(results => {
                return results.json();
            }).then(response => {
                console.log(response);
                if (response['status'] == 'success'){
                    this.setState({auth_token:response['auth_token']});
                
                    localStorage.setItem('username', this.state.username);
                    localStorage.setItem('auth_token', this.state.auth_token);

                    // console.log(localStorage.getItem('username'));
                    // console.log(localStorage.getItem('auth_token'));
                     
                     this.setState({redirect:true});
                }
                else {
                    console.log("failed to log in");
                    // TODO: add an invalid username or password update
                    this.setState({error_message:response['message']});
                    console.log(this.state.error_message)
                }
            });
    }

    handleRedirect(){
        if (this.state.redirect){
            return (<Redirect to='/'/>);
        }
    }

    handleError(){
        if (!(this.state.error_message === '')){
            console.log('error')
            return  (
                <div>
                    <Typography style={{color: 'red'}}>
                        {this.state.error_message}
                    </Typography>
                </div>
            );
        }
    }

    handleKeyPress(event){
        if (event.key === 'Enter'){
            this.handleLogin();
        }
    }
    render(){
        const { classes } = this.props;
        return (
            <div>
                <Paper className="grid-containers">
                            <div className={classes.root}>
                                <Typography variant="h4" displayInline style={{color: '#28324C'}}>
                                    Login
                                </Typography>
                            </div>
                            <div>
                            <TextField
                                required
                                id="outlined-required"
                                label="Username"
                                margin="normal"
                                variant="outlined"
                                onChange={(event) => this.handleUserChange(event)}
                                error={!(this.state.error_message === '')}
                            />
                            </div>
                            <div>
                            <TextField
                                required
                                id="outlined-password-input"
                                label="Password"
                                type="password"
                                margin="normal"
                                variant="outlined"
                                onChange={(event) => this.handlePassChange(event)}
                                error={!(this.state.error_message === '')}
                                onKeyDown={ (event) => this.handleKeyPress(event)}
                            />
                            </div>
                            <div>
                            {this.handleRedirect()}  
                            </div>
                            <div>
                            <Button 
                                onClick={ () => this.handleLogin()}
                                variant="contained"
                                className={classes.button}
                            >
                                Submit
                            </Button>
                            </div>
                            <div>
                            {this.handleError()}
                            </div>
                </Paper>
            </div>
        )
    }
}

export default withStyles(styles)(Login);