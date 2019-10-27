import React from 'react'

import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

// inspired by https://www.cssscript.com/minimal-digital-clock-javascript-css/
const Countdown = (props) => {
	return (
		<div>
		  <Paper className="grid-containers">
		  		<div className="container-text">
		  		  <Table aria-label="simple table">
		  		  	<TableHead>
                      <TableRow>
                      	<TableCell align="left" padding="none" style={{ borderBottom: 'solid 1px #4bacb8'}}><h5>Until Next Passover</h5></TableCell>
                        <TableCell align="center" padding="none" style={{ borderBottom: 'solid 1px #4bacb8'}}><h5>12</h5></TableCell>
                        <TableCell align="center" padding="none" style={{ borderBottom: 'solid 1px #4bacb8'}}><h5>:</h5></TableCell>
                        <TableCell align="center" padding="none" style={{ borderBottom: 'solid 1px #4bacb8'}}><h5>12</h5></TableCell>
                        <TableCell align="center" padding="none" style={{ borderBottom: 'solid 1px #4bacb8'}}><h5>:</h5></TableCell>
                        <TableCell align="center" padding="none" style={{ borderBottom: 'solid 1px #4bacb8'}}><h5>12</h5></TableCell>
                      </TableRow>
                    </TableHead>
		  		  </Table>
		  		</div>
		  </Paper>
        </div>
	)
}

export default Countdown;