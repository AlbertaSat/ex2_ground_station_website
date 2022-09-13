import { makeStyles, TextField } from '@material-ui/core';
import React from 'react';
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';

const FAKE_FILES = [
  { name: 'Test_File_1.txt', size: '69kb', link: 'links not supported yet :(' },
  { name: 'Test_File_2.txt', size: '42kb', link: 'links not supported yet :(' },
  {
    name: 'Test_File_3.txt',
    size: '420kb',
    link: 'links not supported yet :('
  },
  { name: 'Test_File_4.txt', size: '1mb', link: 'links not supported yet :(' },
  { name: 'Test_File_5.txt', size: '666kb', link: 'links not supported yet :(' }
];

const useStyles = makeStyles((theme) => ({
  ftpContainer: {
    display: 'flex',
    justifyContent: 'space-evenly'
  },
  section: {
    display: 'inline-block',
    width: '45%'
  },
  table: {
    minWidth: 325,
    maxWidth: 325
  },
  file: {
    textDecoration: 'underline'
  },
  paper: {}
}));

const FTP = () => {
  const classes = useStyles();

  return (
    <div className={classes.ftpContainer}>
      <div className={classes.section}>
        <Paper className={classes.paper}>
          <div style={{ padding: '20px', textAlign: 'center' }}>
            <Typography variant="h4" style={{ color: '#283246' }}>
              Upload File
            </Typography>
            <input type="file" />
            <Button
              style={{ color: '#118851', marginTop: '10px' }}
              variant="contained"
              name="req-file"
            >
              Upload
            </Button>
          </div>
        </Paper>
      </div>
      <div className={classes.section}>
        <Paper className={classes.paper}>
          <div style={{ padding: '20px', textAlign: 'center' }}>
            <Typography variant="h4" style={{ color: '#283246' }}>
              Download File
            </Typography>
            <Typography variant="caption" style={{ color: '#283246' }}>
              Please click the file you want to download, or use the box below
              to request a file from the satellite.
            </Typography>
            <Table
              size="small"
              aria-label="dense table"
              className={classes.table}
            >
              <TableHead>
                <TableRow>
                  <TableCell style={{ fontWeight: 'bold' }}>
                    File Name
                  </TableCell>
                  <TableCell style={{ fontWeight: 'bold' }}>Size</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {FAKE_FILES.map((file, idx) => (
                  <TableRow key={idx}>
                    <TableCell
                      width="20%"
                      component="th"
                      scope="row"
                      className={classes.file}
                    >
                      {/* TODO: Clicking on a file name should download it */}
                      <a
                        onClick={() => alert('Downloads not supported yet :(')}
                      >
                        {file.name}
                      </a>
                    </TableCell>
                    <TableCell width="20%" component="th" scope="row">
                      {file.size}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            <TextField label="File Name" />
            <Button
              style={{ color: '#118851', marginTop: '10px' }}
              variant="contained"
              name="req-file"
            >
              Request File
            </Button>
          </div>
        </Paper>
      </div>
    </div>
  );
};

export default FTP;
