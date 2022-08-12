import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';


class ResetPassword extends Component {
    constructor() {
        super();
        this.state = {
            newpassword: null,
            newpassword2: null,
            error_message : '',
            success_message: ''
        }
        this.handleNewPasswordChange = this.handleNewPasswordChange.bind(this);
        this.handleNewPassword2Change = this.handleNewPassword2Change.bind(this);
    }



    handleResetPassword() {
        event.preventDefault();
        if (this.state.newpassword !== this.state.newpassword2) {
            this.setState({
                error_message: 'Passwords do not match.',
                success_message: ''
            });
            return;
        }
        
        let auth_token
        if (!!sessionStorage.getItem('auth_token')) {
            auth_token = sessionStorage.getItem('auth_token');
        }
        if (!!localStorage.getItem('auth_token')) {
            sessionStorage.setItem('auth_token', localStorage.getItem('auth_token'));
            auth_token = localStorage.getItem('auth_token');
          }

        const post_data = {
            password: this.state.newpassword
        }
        fetch('/api/users/' + auth_token, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization':'Bearer '+ sessionStorage.getItem('auth_token')
              },
            body: JSON.stringify(post_data),
        }).then(results => {
            return results.json();
        }).then(data => {
            if (data.status == 'success') {
                this.setState({
                    success_message: 'Password was successfully changed.',
                    newpassword: '',
                    newpassword2: '',
                    error_message: ''
                });
            } else {
                console.error('Unexpected error occurred.');
                console.error(data);
                this.setState({
                    error_message: 'An error occurred. Password was not changed successfully.',
                    success_message: ''
                });
            }
        })
    }

    handleKeyPress(event) {
        if (event.key === 'Enter') {
            this.handleResetPassword();
        }
    }

    handleError(){
        if (!(this.state.error_message === '')){
            
            console.log('error')
            return  (
                <div>
                    <Typography style={{color: "red"}}>
                        {this.state.error_message}
                    </Typography>
                </div>
            );
        }
    }

    handleSuccess() {
        if (!(this.state.success_message === '')){
            console.log('success')
            return  (
                <div>
                    <Typography style={{color: "green"}}>
                        {this.state.success_message}
                    </Typography>
                </div>
            );
        }
    }



    handleNewPasswordChange(event) {
        this.setState({newpassword: event.target.value});
    }

    handleNewPassword2Change(event) {
        this.setState({newpassword2: event.target.value});
    }

    render(){
        const { classes } = this.props;
        return (
            <Paper className="grid-containers resetpassword-container">
                <div>
                    <div style={{padding: "20px", textAlign: "center"}}>
                        <Typography variant="h4" style={{color: "#28324C"}}>
                            Reset Password
                        </Typography>
                    </div>
                    
                    <div style={{textAlign: "center"}}>
                        <TextField
                            style={{width: "60%"}}
                            required
                            id="outlined-newpassword-input"
                            label="New Password"
                            type="password"
                            name="password"
                            margin="normal"
                            variant="outlined"
                            value={this.state.newpassword}
                            onChange={(event) => this.handleNewPasswordChange(event)}
                            error={!(this.state.error_message === '')}
                        />
                    </div>
                    <div style={{textAlign: "center"}}>
                        <TextField
                            style={{width: "60%"}}
                            required
                            id="outlined-newpassword2-input"
                            label="Confirm New Password"
                            type="password"
                            name="password"
                            margin="normal"
                            variant="outlined"
                            value={this.state.newpassword2}
                            onChange={(event) => this.handleNewPassword2Change(event)}
                            error={!(this.state.error_message === '')}
                            onKeyDown={ (event) => this.handleKeyPress(event)}
                        />
                    </div>
                    <div>
                        {this.handleError()}
                    </div>
                    
                    <div style = {{display: "flex", alignItems: "center", justifyContent: "center"}}>
                        <Button
                            style={{color: "#118851", marginTop: "10px"}}
                            onClick={ () => this.handleResetPassword()}
                            variant="contained"
                            name="submit"
                        >
                            Submit
                        </Button>
                    </div>
                    <div>
                        {this.handleSuccess()}
                    </div>
                </div>
            </Paper>
        )
    }
}


export default ResetPassword;
