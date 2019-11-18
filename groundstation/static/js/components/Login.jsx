import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
// import Visibility from '@material-ui/icons/Visibility';
// import VisibilityOff from '@material-ui/icons/VisibilityOff';
// const Login = () => (
//   <div>
//     <h1>This is our Login test</h1>
//   </div>
// )

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
            password : null
        }
        this.handleUserChange = this.handleUserChange.bind(this);
        this.handlePassChange = this.handlePassChange.bind(this);
        this.handleLogin = this.handleLogin.bind(this);
    };

    handleUserChange(event){
        this.setState({username: event.target.value});
    }

    handlePassChange(event){
        this.setState({password: event.target.value});
    }

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
            }).then(response => {console.log(response)});
    }

    render(){
        const { classes } = this.props;
        return (
            <div>
                <Grid container spacing={2} alignItems='flex-end'>
                    <Grid item xs={12}>
                        <div className={classes.root}>
                            <Typography variant="h4" displayInline style={{color: '#28324C'}}>
                                Login
                            </Typography>
                        </div>
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            required
                            id="outlined-required"
                            label="Username"
                            margin="normal"
                            variant="outlined"
                            onChange={(event) => this.handleUserChange(event)}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            required
                            id="outlined-password-input"
                            label="Password"
                            type="password"
                            margin="normal"
                            variant="outlined"
                            onChange={(event) => this.handlePassChange(event)}
                        />
                    </Grid>
                    <Grid item xs={12}>    
                        <Button 
                            onClick={ () => this.handleLogin()}
                            variant="contained"
                            className={classes.button}
                        >
                            Submit
                        </Button>
                    </Grid>
                </Grid>
            </div>
        )
    }
}

export default withStyles(styles)(Login);