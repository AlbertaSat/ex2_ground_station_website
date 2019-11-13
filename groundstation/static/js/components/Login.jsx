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
    };

    // ComponentDidMount(){

    // }
    handleUserChange(event){
        this.setState({username: event.target.value});

        console.log(event.target.value)
    }

    // handlePassChange:function(info){
    //     this.setState({password: info.target.value})
    // },

    // handleLogin(event){
    //     event.preventDefault();
    //     let data = {username:this.state.username, password:this.state.password}
    //     fetch('/api/auth/login')
    // }

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
                            autoComplete="example@email.com"
                            className={classes.textField}
                            margin="normal"
                            variant="outlined"
                            value={this.state.username}
                            onChange={this.handleUserChange}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            required
                            id="outlined-password-input"
                            label="Password"
                            className={classes.textField}
                            type="password"
                            autoComplete="current-password"
                            margin="normal"
                            variant="outlined"
                            value={this.state.password}
                        />
                    </Grid>
                    <Grid item xs={12}>    
                        <Button 
                            variant="contained"
                            color="primary"
                            className={classes.button}
                        >
                            Submit
                        </Button>
                    </Grid>
                </Grid>
                /*<div>
                    <Button 
                        variant="contained"
                        color="primary"
                        className={classes.button}
                    >
                        Submit
                    </Button>
                </div>*/
            </div>
        )
    }
}

export default withStyles(styles)(Login);