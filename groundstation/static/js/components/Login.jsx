import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
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

        }

    };

    // ComponentDidMount(){

    // }
    // handleLogin(event){
    //     event.preventDefault();
        
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
                            label="Email"
                            autoComplete="example@email.com"
                            className={classes.textField}
                            margin="normal"
                            variant="outlined"
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
                        />
                    </Grid>
                </Grid>
            </div>
        )
    }
}

export default withStyles(styles)(Login);