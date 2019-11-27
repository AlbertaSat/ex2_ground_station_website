import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';

class Help extends Component {
    constructor(){
        super();
        this.state = {
        }
    }

    render(){
        return (
            <div>
                <Typography variant="h4" style={{color: '#28324C'}}>
                    Help Page
                </Typography>
            </div>
        )
    }
}

export default Help;