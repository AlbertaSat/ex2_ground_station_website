import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
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

    render(){
        const { classes } = this.props;
        return (
            <div>
                <Grid container spacing={2} alignItems='flex-end'>
                    <Grid item sm={8}>
                        <div className={classes.root}>
                            <Typography variant="h4" displayInline style={{color: '#28324C'}}>
                                Login
                            </Typography>
                        </div>
                    </Grid>
                </Grid>
            </div>
        )
    }
}

export default withStyles(styles)(Login);