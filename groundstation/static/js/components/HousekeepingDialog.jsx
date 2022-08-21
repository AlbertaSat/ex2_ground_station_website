import React, { useRef } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Dialog from '@material-ui/core/Dialog';
import { Grid } from '@material-ui/core';
import ListItemText from '@material-ui/core/ListItemText';
import ListItem from '@material-ui/core/ListItem';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Slide from '@material-ui/core/Slide';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%'
  },
  appBar: {
    position: 'sticky'
  },
  title: {
    marginLeft: theme.spacing(2),
    flex: 1
  },
  subtitle: {
    marginLeft: theme.spacing(2)
  },
  paper: {
    marginTop: theme.spacing(3),
    width: '100%',
    overflowX: 'auto',
    marginBottom: theme.spacing(2)
  },
  table: {
    minWidth: 650
  },
  customListItemText: {
    display: 'flex',
    alignItems: 'baseline',
    justifyContent: 'space-between',
    maxWidth: '78%'
  },
  navbarLinks: {
    color: '#fff',
    '&:hover': {
      color: '#55c4d3'
    }
  }
}));

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const HousekeepingDialog = (props) => {
  const classes = useStyles();

  const adcsRef = useRef();
  const athenaRef = useRef();
  const epsRef = useRef();
  const epsStartupRef = useRef();
  const uhfRef = useRef();
  const sbandRef = useRef();
  const hyperionRef = useRef();
  const charonRef = useRef();
  const dfgmRef = useRef();
  const nsRef = useRef();
  const irisRef = useRef();

  /**
   * Scrolls the page to a given section
   * @param {React.MutableRefObject} section The section to scroll to
   */
  const handleScrollClick = (section) => {
    section.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  return (
    /* Display a HK log in a full screen dialog */
    <Dialog
      fullScreen
      open={props.open}
      onClose={() => props.handleClose()}
      TransitionComponent={Transition}
    >
      <AppBar className={classes.appBar}>
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            onClick={() => props.handleClose()}
            aria-label="close"
          >
            <CloseIcon />
          </IconButton>
          <Typography variant="h6" className={classes.title}>
            {props.housekeeping.timestamp}
          </Typography>
          <Typography
            className="menu-links"
            style={{ display: 'inline-flex', alignItems: 'center' }}
          >
            <a
              className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
              onClick={() => handleScrollClick(adcsRef)}
            >
              ADCS
            </a>
            <a
              className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
              onClick={() => handleScrollClick(athenaRef)}
            >
              Athena
            </a>
            <a
              className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
              onClick={() => handleScrollClick(epsRef)}
            >
              EPS
            </a>
            <a
              className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
              onClick={() => handleScrollClick(epsStartupRef)}
            >
              EPS Startup
            </a>
            <a
              className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
              onClick={() => handleScrollClick(uhfRef)}
            >
              UHF
            </a>
            <a
              className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
              onClick={() => handleScrollClick(sbandRef)}
            >
              S-Band
            </a>
            <a
              className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
              onClick={() => handleScrollClick(hyperionRef)}
            >
              Hyperion
            </a>
            <a
              className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
              onClick={() => handleScrollClick(charonRef)}
            >
              Charon
            </a>
            <a
              className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
              onClick={() => handleScrollClick(dfgmRef)}
            >
              DFGM
            </a>
            <a
              className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
              onClick={() => handleScrollClick(nsRef)}
            >
              Northern Spirit
            </a>
            <a
              className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
              onClick={() => handleScrollClick(irisRef)}
            >
              IRIS
            </a>
          </Typography>
        </Toolbar>
      </AppBar>

      {/* General info about HK data */}
      <List>
        <ListItem>
          <ListItemText
            classes={{ root: classes.customListItemText }}
            primary="Data Position"
            secondary={props.housekeeping.data_position}
          />
        </ListItem>
        <ListItem>
          <ListItemText
            classes={{ root: classes.customListItemText }}
            primary="TLE"
            secondary={props.housekeeping.tle}
          />
        </ListItem>
      </List>

      <br></br>

      <Typography variant="h4" className={classes.subtitle} ref={adcsRef}>
        ADCS
      </Typography>
      <List>
        <Grid container spacing={2}>
          {Object.keys(props.housekeeping.adcs).map((label) => (
            <Grid item>
              <ListItem>
                <ListItemText
                  primary={label}
                  secondary={props.housekeeping.adcs[label]}
                />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </List>

      <br></br>

      <Typography variant="h4" className={classes.subtitle} ref={athenaRef}>
        Athena
      </Typography>
      <List>
        <Grid container spacing={2}>
          {Object.keys(props.housekeeping.athena).map((label) => (
            <Grid item>
              <ListItem>
                <ListItemText
                  primary={label}
                  secondary={props.housekeeping.athena[label]}
                />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </List>

      <br></br>

      <Typography variant="h4" className={classes.subtitle} ref={epsRef}>
        EPS
      </Typography>
      <List>
        <Grid container spacing={2}>
          {Object.keys(props.housekeeping.eps).map((label) => (
            <Grid item>
              <ListItem>
                <ListItemText
                  primary={label}
                  secondary={props.housekeeping.eps[label]}
                />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </List>

      <br></br>

      <Typography variant="h5" className={classes.subtitle} ref={epsStartupRef}>
        EPS Startup
      </Typography>
      <List>
        <Grid container spacing={2}>
          {Object.keys(props.housekeeping.eps_startup).map((label) => (
            <Grid item>
              <ListItem>
                <ListItemText
                  primary={label}
                  secondary={props.housekeeping.eps_startup[label]}
                />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </List>

      <br></br>

      <Typography variant="h4" className={classes.subtitle} ref={uhfRef}>
        UHF
      </Typography>
      <List>
        <Grid container spacing={2}>
          {Object.keys(props.housekeeping.uhf).map((label) => (
            <Grid item>
              <ListItem>
                <ListItemText
                  primary={label}
                  secondary={props.housekeeping.uhf[label]}
                />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </List>

      <br></br>

      <Typography variant="h4" className={classes.subtitle} ref={sbandRef}>
        S-Band
      </Typography>
      <List>
        <Grid container spacing={2}>
          {Object.keys(props.housekeeping.sband).map((label) => (
            <Grid item>
              <ListItem>
                <ListItemText
                  primary={label}
                  secondary={props.housekeeping.sband[label]}
                />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </List>

      <br></br>

      <Typography variant="h4" className={classes.subtitle} ref={hyperionRef}>
        Hyperion
      </Typography>
      <List>
        <Grid container spacing={2}>
          {Object.keys(props.housekeeping.hyperion).map((label) => (
            <Grid item>
              <ListItem>
                <ListItemText
                  primary={label}
                  secondary={props.housekeeping.hyperion[label]}
                />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </List>

      <br></br>

      <Typography variant="h4" className={classes.subtitle} ref={charonRef}>
        Charon
      </Typography>
      <List>
        <Grid container spacing={2}>
          {Object.keys(props.housekeeping.charon).map((label) => (
            <Grid item>
              <ListItem>
                <ListItemText
                  primary={label}
                  secondary={props.housekeeping.charon[label]}
                />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </List>

      <br></br>

      <Typography variant="h4" className={classes.subtitle} ref={dfgmRef}>
        DFGM
      </Typography>
      <List>
        <Grid container spacing={2}>
          {Object.keys(props.housekeeping.dfgm).map((label) => (
            <Grid item>
              <ListItem>
                <ListItemText
                  primary={label}
                  secondary={props.housekeeping.dfgm[label]}
                />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </List>

      <br></br>

      <Typography variant="h4" className={classes.subtitle} ref={nsRef}>
        Northern Spirit
      </Typography>
      <List>
        <Grid container spacing={2}>
          {Object.keys(props.housekeeping.northern_spirit).map((label) => (
            <Grid item>
              <ListItem>
                <ListItemText
                  primary={label}
                  secondary={props.housekeeping.northern_spirit[label]}
                />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </List>

      <br></br>

      <Typography variant="h4" className={classes.subtitle} ref={irisRef}>
        IRIS
      </Typography>
      <List>
        <Grid container spacing={2}>
          {Object.keys(props.housekeeping.iris).map((label) => (
            <Grid item>
              <ListItem>
                <ListItemText
                  primary={label}
                  secondary={props.housekeeping.iris[label]}
                />
              </ListItem>
            </Grid>
          ))}
        </Grid>
      </List>
    </Dialog>
  );
};

export default HousekeepingDialog;
