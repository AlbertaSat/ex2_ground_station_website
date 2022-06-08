import React, { useEffect, createRef, useState } from 'react'
import Button from '@material-ui/core/Button';
import {formatDateToUTCString} from '../helpers.js'


const CommunicationEntry = (props) => {
    const [isQueued, setIsQueued] = useState(props.entry.is_queued);

    const showQueueButton = props.showQueueButton;

    function queueHandler() {
        const patch_queue = {
            is_queued: !props.entry.is_queued
        }
        fetch(`/api/communications/${props.entry.message_id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization':'Bearer '+ sessionStorage.getItem('auth_token')
            } ,
            body: JSON.stringify(patch_queue),
        }).then(results => {
            return results.json();
        }).then(data => {
            if (data.status === 'success') {
                props.entry.is_queued = !props.entry.is_queued;
                setIsQueued(props.entry.is_queued);
            } else {
                console.error('Unexpected error occured:');
            }
        });
    }

    const divStyle = {
        paddingBottom:'1%',
        paddingLeft:'1%',
        paddingRight:'1%',
    };
    const contentStyle = {};
    const infoStringStyle = {};

    const username = sessionStorage.getItem('username');

    const sender = props.entry.sender;
    console.log(props.entry)

    let infoStringPrefix;
    let infoTimestamp;

    if (sender === 'comm') {
        divStyle.backgroundColor = '#e3e3e3';
        contentStyle.color = '#007b40';
        infoStringPrefix = 'Message from';
    } else {
        divStyle.backgroundColor = '#f2f2f2';
        contentStyle.color = '#56b2bc';
        infoStringPrefix = 'Input from';
    }

    // this is pre janky but its the way it is
    infoTimestamp = props.entry.timestamp;
    if (infoTimestamp[infoTimestamp.length - 1] !== 'Z') {
        infoTimestamp = infoTimestamp + 'Z';
    }
    infoTimestamp = new Date(infoTimestamp);
    let infoStringTimestamp = formatDateToUTCString(infoTimestamp);

    return (
        <div style={divStyle}>
            <div>
                <p style={infoStringStyle}>{infoStringPrefix} <strong>{sender}</strong> on: </p><p>{infoStringTimestamp}</p>
            </div>
            <p style={contentStyle}>Message: {props.entry.message}</p>
            {((sender === 'comm') || !showQueueButton) ? null: <p style={contentStyle}>Is Queued: {isQueued ? 'true' : 'false'}</p>}
            <div>
            {((props.is_admin || (sender === username)) && (sender !== 'comm') && (showQueueButton)) ? <Button
                style={{marginBottom:"1%"}}
                color = "primary"
                onClick={queueHandler}
                variant = 'outlined'>{props.entry.is_queued ? 'De-Queue': 'Queue'}</Button>: null}
            </div>
        </div>
    );
}


const CommunicationsList = (props) => {
    const [isAdmin, setIsAdmin] = useState(false);

    const divStyle = {margin:'2%'}

    console.log(props.showQueueButton);

    const messagesEndRef = createRef();
    if (props.autoScroll === true) {
        const scrollToBottom = () => {
            messagesEndRef.current.scrollIntoView({behavior: 'smooth'});
        };
        useEffect(scrollToBottom, [props.displayLog]);
    }

	if (props.isEmpty) {
      return (
        <div style={divStyle}>
        	No Messages to display
        </div>
      )
    }


    const auth_token = sessionStorage.getItem('auth_token');
    fetch(`/api/users/${auth_token}`).then(results => {
        return results.json();
    }).then(data => {
        if (data.status === 'success') {
            setIsAdmin(data.data.is_admin);
        } else {
            console.error('Unexpected error occured:');
        }
    });


	return (
        <div style={divStyle}>
            {props.displayLog.map(logEntry => (
                <CommunicationEntry entry={logEntry} is_admin={isAdmin} showQueueButton={props.showQueueButton}/>
            ))}
            <div ref={messagesEndRef} />
        </div>
    );
}

export default CommunicationsList;
