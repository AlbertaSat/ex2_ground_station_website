import { makeStyles, Paper, Typography } from '@material-ui/core';
import React from 'react';

const useStyles = makeStyles((theme) => ({
  ftpContainer: {
    display: 'flex',
    justifyContent: 'space-evenly'
  },
  section: {
    display: 'inline-block',
    width: '45%'
  },
  paper: {}
}));

const FTP = () => {
  const classes = useStyles();

  return (
    <div className={classes.ftpContainer}>
      <div className={classes.section}>
        <Paper className={classes.paper}>
          <div>
            <div style={{ padding: '20px', textAlign: 'center' }}>
              <Typography variant="h4" style={{ color: '#283246' }}>
                Upload File
              </Typography>
            </div>
          </div>
        </Paper>
      </div>
      <div className={classes.section}>
        <Paper className={classes.paper}>
          <div>
            <div style={{ padding: '20px', textAlign: 'center' }}>
              <Typography variant="h4" style={{ color: '#283246' }}>
                Download File
              </Typography>
            </div>
          </div>
        </Paper>
      </div>
    </div>
  );
};

export default FTP;
