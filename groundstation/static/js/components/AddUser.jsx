import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from "@material-ui/core/Checkbox";
import Paper from '@material-ui/core/Paper';

const styles = {
    root: {
      padding: '20px',
      textAlign: "center"
    },
    buttonDivCenter: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    },
  };

class AddUser extends Component {
    constructor() {
        super();
        this.state = {
            error_message : '',
            newUserIsAdmin: false,
            success_message: ''
        }
        this.usernameRef = React.createRef();
        this.passwordRef = React.createRef();
        this.confirmPasswordRef = React.createRef();
    }


    handleAddUser() {
        event.preventDefault();
        if (this.passwordRef.current.value !== this.confirmPasswordRef.current.value) {
            this.setState({error_message: "Passwords do not match."});
            return;
        }
        console.log(this.usernameRef.current.value); //undefined. child element might not be in DOM or whatever
        console.log(this.passwordRef.current.value); // undefined
        const post_data = {
            username: this.usernameRef.current.value,
            password: this.passwordRef.current.value,
            //is_admin: this.state.newUserIsAdmin
        }
        fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization':'Bearer '+ sessionStorage.getItem('auth_token')
              },
            body: JSON.stringify(post_data),
        }).then(results => {
            return results.json();
        }).then(data => {
            if (data.status == 'success') {
                this.setState({success_message: data.message});
                this.usernameRef.current.value = '';
                this.passwordRef.current.value = '';
                this.confirmPasswordRef.current.value = '';
            } else {
                console.error('Unexpected error occurred.');
                console.error(data);
                this.setState({error_message: data.message});
            }
        })
    }

    handleKeyPress(event) {
        if (event.key === 'Enter') {
            this.handleAddUser();
        }
    }

    handleChecked(event) {
        this.setState({newUserIsAdmin: event.target.checked});
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

    handleSuccess() {
        if (!(this.state.success_message === '')){
            console.log('success')
            return  (
                <div>
                    <Typography style={{color: 'green'}}>
                        {this.state.success_message}
                    </Typography>
                </div>
            );
        }
    }

    render(){
        const { classes } = this.props;
        return (
            <Paper className="grid-containers adduser-container">
                <div>
                    <div className={classes.root}>
                        <Typography variant="h4" style={{color: '#28324C'}}>
                            Register New User
                        </Typography>
                    </div>
                    
                    <div>
                        <TextField
                            style={{width: "100%"}}
                            required
                            id="outlined-required"
                            label="Username"
                            name="username"
                            margin="normal"
                            variant="outlined"
                            ref = {this.usernameRef}
                            error={!(this.state.error_message === '')}
                        />
                    </div>
                    <div>
                        <TextField
                            style={{width: "100%"}}
                            required
                            id="outlined-password-input"
                            label="Password"
                            type="password"
                            name="password"
                            margin="normal"
                            variant="outlined"
                            ref = {this.passwordRef}
                            error={!(this.state.error_message === '')}
                        />
                    </div>
                    <div>
                        <TextField
                            style={{width: "100%"}}
                            required
                            id="outlined-confirmpassword-input"
                            label="Confirm Password"
                            type="password"
                            name="password"
                            margin="normal"
                            variant="outlined"
                            ref = {this.confirmPasswordRef}
                            error={!(this.state.error_message === '')}
                            onKeyDown={ (event) => this.handleKeyPress(event)}
                        />
                    </div>
                    <div>
                        {this.handleError()}
                    </div>
                    <div>
                        <FormControlLabel label="Admin User"
                            control={<Checkbox checked={this.state.newUserIsAdmin} onChange={(event) => this.handleChecked(event)} />} />
                    </div>
                    <div>
                        {this.handleSuccess()}
                    </div>
                    <div className={classes.buttonDivCenter}>
                        <Button
                            style={{color: "#118851", marginTop: "10px"}}
                            onClick={ () => this.handleAddUser()}
                            variant="contained"
                            name="submit"
                        >
                            Submit
                        </Button>
                    </div>
                </div>
            </Paper>
        )
    }
}


export default withStyles(styles)(AddUser); // maybe export as default and define component as function?