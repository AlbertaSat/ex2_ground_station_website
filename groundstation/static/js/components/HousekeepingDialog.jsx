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

const DECIMAL_PLACES = 5; // How many decimal places to round floats to

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
    minWidth: 325,
    maxWidth: 325
  },
  label: {
    fontWeight: 600
  },
  hkDisplay: {
    columnSpan: 'none',
    columnCount: 4,
    columnWidth: 300
  },
  hkItem: {
    breakInside: 'avoid-column'
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

  /**
   * Rounds housekeeeping values to 3 decimal places to keep tables thin
   *
   * @param value A value to potentially round
   * @returns A value rounded to 3 decimals (if possible)
   */
  const roundValue = (value) => {
    return Number(value) === value && value % 1 !== 0
      ? value.toFixed(DECIMAL_PLACES)
      : value;
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

      <div className={classes.hkDisplay}>
        <div className={classes.hkItem}>
          <Typography variant="h4" className={classes.subtitle} ref={adcsRef}>
            ADCS
          </Typography>
          <Table
            className={classes.table}
            size="small"
            aria-label="dense table"
          >
            <TableBody>
              {Object.keys(props.housekeeping.adcs).map((label, idx) => (
                <TableRow key={idx}>
                  <TableCell
                    width="20%"
                    component="th"
                    scope="row"
                    className={classes.label}
                  >
                    {label}
                  </TableCell>
                  <TableCell width="60%" align="left">
                    {roundValue(props.housekeeping.adcs[label])}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <br></br>

        <div className={classes.hkItem}>
          <Typography variant="h4" className={classes.subtitle} ref={athenaRef}>
            Athena
          </Typography>
          <Table
            className={classes.table}
            size="small"
            aria-label="dense table"
          >
            <TableBody>
              {Object.keys(props.housekeeping.athena).map((label, idx) => (
                <TableRow key={idx}>
                  <TableCell
                    width="20%"
                    component="th"
                    scope="row"
                    className={classes.label}
                  >
                    {label}
                  </TableCell>
                  <TableCell width="60%" align="left">
                    {roundValue(props.housekeeping.athena[label])}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <br></br>

        <div className={classes.hkItem}>
          <Typography variant="h4" className={classes.subtitle} ref={epsRef}>
            EPS
          </Typography>
          <Table
            className={classes.table}
            size="small"
            aria-label="dense table"
          >
            <TableBody>
              {Object.keys(props.housekeeping.eps).map((label, idx) => (
                <TableRow key={idx}>
                  <TableCell
                    width="20%"
                    component="th"
                    scope="row"
                    className={classes.label}
                  >
                    {label}
                  </TableCell>
                  <TableCell width="60%" align="left">
                    {roundValue(props.housekeeping.eps[label])}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <br></br>

        <div className={classes.hkItem}>
          <Typography
            variant="h4"
            className={classes.subtitle}
            ref={epsStartupRef}
          >
            EPS Startup
          </Typography>
          <Table
            className={classes.table}
            size="small"
            aria-label="dense table"
          >
            <TableBody>
              {Object.keys(props.housekeeping.eps_startup).map((label, idx) => (
                <TableRow key={idx}>
                  <TableCell
                    width="20%"
                    component="th"
                    scope="row"
                    className={classes.label}
                  >
                    {label}
                  </TableCell>
                  <TableCell width="60%" align="left">
                    {roundValue(props.housekeeping.eps_startup[label])}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <br></br>

        <div className={classes.hkItem}>
          <Typography variant="h4" className={classes.subtitle} ref={uhfRef}>
            UHF
          </Typography>
          <Table
            className={classes.table}
            size="small"
            aria-label="dense table"
          >
            <TableBody>
              {Object.keys(props.housekeeping.uhf).map((label, idx) => (
                <TableRow key={idx}>
                  <TableCell
                    width="20%"
                    component="th"
                    scope="row"
                    className={classes.label}
                  >
                    {label}
                  </TableCell>
                  <TableCell width="60%" align="left">
                    {roundValue(props.housekeeping.uhf[label])}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <br></br>

        <div className={classes.hkItem}>
          <Typography variant="h4" className={classes.subtitle} ref={sbandRef}>
            S-Band
          </Typography>
          <Table
            className={classes.table}
            size="small"
            aria-label="dense table"
          >
            <TableBody>
              {Object.keys(props.housekeeping.sband).map((label, idx) => (
                <TableRow key={idx}>
                  <TableCell
                    width="20%"
                    component="th"
                    scope="row"
                    className={classes.label}
                  >
                    {label}
                  </TableCell>
                  <TableCell width="60%" align="left">
                    {roundValue(props.housekeeping.sband[label])}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <br></br>

        <div className={classes.hkItem}>
          <Typography
            variant="h4"
            className={classes.subtitle}
            ref={hyperionRef}
          >
            Hyperion
          </Typography>
          <Table
            className={classes.table}
            size="small"
            aria-label="dense table"
          >
            <TableBody>
              {Object.keys(props.housekeeping.hyperion).map((label, idx) => (
                <TableRow key={idx}>
                  <TableCell
                    width="20%"
                    component="th"
                    scope="row"
                    className={classes.label}
                  >
                    {label}
                  </TableCell>
                  <TableCell width="60%" align="left">
                    {roundValue(props.housekeeping.hyperion[label])}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <br></br>

        <div className={classes.hkItem}>
          <Typography variant="h4" className={classes.subtitle} ref={charonRef}>
            Charon
          </Typography>
          <Table
            className={classes.table}
            size="small"
            aria-label="dense table"
          >
            <TableBody>
              {Object.keys(props.housekeeping.charon).map((label, idx) => (
                <TableRow key={idx}>
                  <TableCell
                    width="20%"
                    component="th"
                    scope="row"
                    className={classes.label}
                  >
                    {label}
                  </TableCell>
                  <TableCell width="60%" align="left">
                    {roundValue(props.housekeeping.charon[label])}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <br></br>

        <div className={classes.hkItem}>
          <Typography variant="h4" className={classes.subtitle} ref={dfgmRef}>
            DFGM
          </Typography>
          <Table
            className={classes.table}
            size="small"
            aria-label="dense table"
          >
            <TableBody>
              {Object.keys(props.housekeeping.dfgm).map((label, idx) => (
                <TableRow key={idx}>
                  <TableCell
                    width="20%"
                    component="th"
                    scope="row"
                    className={classes.label}
                  >
                    {label}
                  </TableCell>
                  <TableCell width="60%" align="left">
                    {roundValue(props.housekeeping.dfgm[label])}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <br></br>

        <div className={classes.hkItem}>
          <Typography variant="h4" className={classes.subtitle} ref={nsRef}>
            Northern Spirit
          </Typography>
          <Table
            className={classes.table}
            size="small"
            aria-label="dense table"
          >
            <TableBody>
              {Object.keys(props.housekeeping.northern_spirit).map(
                (label, idx) => (
                  <TableRow key={idx}>
                    <TableCell
                      width="20%"
                      component="th"
                      scope="row"
                      className={classes.label}
                    >
                      {label}
                    </TableCell>
                    <TableCell width="60%" align="left">
                      {roundValue(props.housekeeping.northern_spirit[label])}
                    </TableCell>
                  </TableRow>
                )
              )}
            </TableBody>
          </Table>
        </div>

        <br></br>

        <div className={classes.hkItem}>
          <Typography variant="h4" className={classes.subtitle} ref={irisRef}>
            IRIS
          </Typography>
          <Table
            className={classes.table}
            size="small"
            aria-label="dense table"
          >
            <TableBody>
              {Object.keys(props.housekeeping.iris).map((label, idx) => (
                <TableRow key={idx}>
                  <TableCell
                    width="20%"
                    component="th"
                    scope="row"
                    className={classes.label}
                  >
                    {label}
                  </TableCell>
                  <TableCell width="60%" align="left">
                    {roundValue(props.housekeeping.iris[label])}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </Dialog>
  );
};

export default HousekeepingDialog;
