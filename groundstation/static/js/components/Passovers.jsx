import React from 'react'

import LinearProgress from '@material-ui/core/LinearProgress';
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import {formatDateToUTCString} from '../helpers.js'

const useStyles = makeStyles(theme => ({
  root: {
    width: '100%',
  },
  title: {
    marginLeft: theme.spacing(2),
    flex: 1,
  },
  paper: {
    marginTop: theme.spacing(3),
    width: '100%',
    overflowX: 'auto',
    marginBottom: theme.spacing(2),
  },
}));

function calculateProgessBar(startTime, currentTime, endTime) {
    let maxDifference = endTime - startTime;
    let progress = currentTime - startTime;
    let progressPercent = Math.min((progress / maxDifference) * 100, 100);
    return progressPercent.toString();
}

const Passovers = (props) => {
	if (props.isLoading) {
    return (
      <div>
        <LinearProgress />
      </div>
    )
	}

  if (props.empty && !props.isLoading) {
    return (
      <div>
        <ErrorOutlineIcon /> There is currently no upcoming passovers!
      </div>
    )
  }

  const classes = useStyles();

  return (
  	<div className={classes.root}>
  	  <Paper className={classes.paper}>
  	    {props.passovers.map(passover => (
	  	   <Table aria-label="simple table">
		  	  <TableBody>
		        <TableRow key={passover.passover_id} id={"passover-" + passover.passover_id}>
                    <div>
    		           <TableCell width="15%" component="th" scope="row">
    		              {formatDateToUTCString(new Date(passover.timestamp + 'Z'))}
    		           </TableCell>
                   </div>
                   <div>
                       <LinearProgress color="secondary" variant="determinate" value={calculateProgessBar(new Date(props.mostRecentPass.timestamp + 'Z'), new Date(), new Date(passover.timestamp + 'Z'))} />
                   </div>
               </TableRow>
		      </TableBody>
	       </Table>
    	))}
  	  </Paper>
  	</div>
  )

}

export default Passovers;
