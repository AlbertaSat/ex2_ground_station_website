import React from 'react'
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import LinearProgress from '@material-ui/core/LinearProgress';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import ArrowDropUpIcon from '@material-ui/icons/ArrowDropUp';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';

const AutomatedCommandSequenceList = (props) => {
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
                <ErrorOutlineIcon /> There are no automated command sequences!
            </div>
        )
    }

    return (
        <div>
            <Table aria-label="simple table" size="small">
                <TableHead>
                    <TableRow>
                        <TableCell style={{fontWeight: "bold"}}>Command Name</TableCell>
                        <TableCell style={{fontWeight: "bold"}} align="right">Navigation</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {props.commands.map((command, idx) => (
                        <TableRow key={idx}>
                            <TableCell component="th" scope="row">
                                {command.name}
                            </TableCell>
                            <TableCell align="right">
                                <IconButton onClick={(event) => props.handleRearrangeClick(event, idx, true)}>
                                    <ArrowDropUpIcon style={{color: '#4bacb8'}} />
                                </IconButton>
                                <IconButton onClick={(event) => props.handleRearrangeClick(event, idx, false)}>
                                    <ArrowDropDownIcon style={{color: '#4bacb8'}} />
                                </IconButton>
                                <IconButton>
                                    <DeleteIcon style={{color: '#4bacb8'}} />
                                </IconButton>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    )
}

export default AutomatedCommandSequenceList;