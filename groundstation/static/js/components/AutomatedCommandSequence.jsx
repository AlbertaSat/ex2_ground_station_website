import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import Fab from '@material-ui/core/Fab';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import HousekeepingList from './HousekeepingListFull';
import Passovers from './Passovers';
import Switch from "@material-ui/core/Switch";
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';
import AddIcon from '@material-ui/icons/Add';
import AutomatedCommandSequenceList from './AutomatedCommandSequenceList';

class AutomatedCommandSequence extends Component {
    constructor() {
        super();
        this.state = {
            isLoading: false,
            empty: false,
            commands: []
        }

        this.state.commands.push({name: "GET-HK"})
        this.state.commands.push({name: "ping"})
        this.state.commands.push({name: "GET-HK"})
        this.state.commands.push({name: "ping"})
        this.state.commands.push({name: "GET-HK"})
        this.state.commands.push({name: "ping"})

        this.handleAddCommandOpenClick = this.handleAddCommandOpenClick.bind(this);
        this.handleRearrangeClick = this.handleRearrangeClick.bind(this);

    }

    componentDidMount() {

    }

    handleAddCommandOpenClick(event) {

    }

    handleRearrangeClick(event, idx, up=false) {
        // handle trying to move the top element up or last element down
        if ((idx == 0 && up == true) || (idx == this.state.commands.length - 1 && up == false)) {
            return;
        } 
        
        let copy = this.state.commands.slice();
        let offset = (up == true) ? -1 : 1;
        let temp = copy[idx];
        copy[idx] = copy[idx + offset];
        copy[idx + offset] = temp;
        this.setState({commands: copy});
    }

    render() {
        return (
            <div>
            <Paper className="grid-containers" style={{marginBottom: '20px'}}>
            <Grid container>
                <Grid item xs={11}>
                    <Typography variant="h5" style={{padding: '10px'}}>Automated Command Sequence</Typography>
                </Grid>
				<Grid item xs={1} style={{textAlign: 'right'}}>
					<Fab style={{position: 'inherit'}} onClick={ (event) => this.handleAddFlightOpenClick(event) }>
						<AddIcon 
								style={{ color: '#4bacb8', fontSize: '2rem'}} 
						/>
					</Fab>
				</Grid>                
            </Grid>    
            </Paper>

            <Grid container style= {{paddingBottom: '12px', justifyContent: 'center'}}>
            <Paper className="grid-containers" style={{minWidth: 650}}>
                <Grid item>
                    <AutomatedCommandSequenceList
                    isLoading={this.state.isLoading}
                    commands={this.state.commands}
                    handleRearrangeClick={this.handleRearrangeClick}
                    empty={this.state.empty}
                    />
                </Grid>
            </Paper>                
            </Grid>
            </div>
        )
    }
}

export default AutomatedCommandSequence;